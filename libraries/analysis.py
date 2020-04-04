import json

from collections import namedtuple

import pandas

from textblob import TextBlob


TripAdvisorReview = namedtuple('TripAdvisorReview', ['id', 'text', 'rating'])


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
