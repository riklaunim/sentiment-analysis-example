import json

from collections import namedtuple

import pandas
import matplotlib.pyplot as plot

from textblob import TextBlob


class SentimentAnalyzer:
    def build_data_set(self, json_file):
        data = self._get_data_frame(json_file)
        data['polarity'] = data['text'].apply(self._get_polarity)
        data['subjectivity'] = data['text'].apply(self._get_subjectivity)
        return data

    @staticmethod
    def _get_data_frame(json_file):
        factory = DataFrameFactory(json_file)
        return factory.get_data_frame()

    @staticmethod
    def _get_polarity(phrase):
        return TextBlob(phrase).sentiment.polarity

    @staticmethod
    def _get_subjectivity(phrase):
        return TextBlob(phrase).sentiment.subjectivity


class DataFrameFactory:
    def __init__(self, json_file):
        self.json_file = json_file

    def get_data_frame(self):
        raw_data = self._get_raw_data()
        return pandas.DataFrame(raw_data, columns=['id', 'text', 'rating'])

    def _get_raw_data(self):
        json_data = self._get_raw_json()
        for review in json_data['data']:
            yield TripAdvisorReview(review['id'], review['attributes']['text'], review['attributes']['rating'])

    def _get_raw_json(self):
        file = open(self.json_file)
        return json.loads(file.read())


TripAdvisorReview = namedtuple('TripAdvisorReview', ['id', 'text', 'rating'])


class SentimentPlotter:
    def __init__(self, data_set):
        self.data_set = data_set

    def draw(self, chart_name='sentiment.png'):
        plot.rcParams['figure.figsize'] = [10, 8]

        for id, text in enumerate(self.data_set.index):
            x = self.data_set.polarity.loc[text]
            y = self.data_set.subjectivity.loc[text]
            plot.scatter(x, y, color='Red')

        plot.title('Sentiment Analysis', fontsize=20)
        plot.xlabel('← Negative — — — — — — Positive →', fontsize=15)
        plot.ylabel('← Facts — — — — — — — Opinions →', fontsize=15)
        plot.savefig(chart_name)


class SentimentPrinter:
    template_file = 'assets/template.html'
    template_block = '<!-- template -->'

    def __init__(self, data_set):
        self.data_set = data_set

    def save(self, file_name='analysis.html'):
        template = open(self.template_file).read()
        rows = self._get_rows()
        html = template.replace(self.template_block, rows)
        new_file = open(file_name, 'w')
        new_file.write(html)
        new_file.close()

    def _get_rows(self):
        rows = []
        data = self.data_set.to_dict(orient='records')
        for row in data:
            row_entry = self.row_template.format(
                row['id'], row['text'], row['rating'], row['subjectivity'], row['polarity'],
            )
            rows.append(row_entry)
        return '\n'.join(rows)

    @property
    def row_template(self):
        return '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
