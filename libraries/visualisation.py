import matplotlib.pyplot as plot


class SentimentPlotter:
    def __init__(self, data_set):
        self.data_set = data_set

    def draw(self, chart_name='sentiment.png'):
        self._configure_chart()
        self._fill_chart()
        plot.savefig(chart_name)
        plot.close()

    @staticmethod
    def _configure_chart():
        plot.rcParams['figure.figsize'] = [10, 8]
        plot.title('Sentiment Analysis', fontsize=20)
        plot.xlabel('← Negative — — — — — — Positive →', fontsize=15)
        plot.ylabel('← Facts — — — — — — — Opinions →', fontsize=15)

    def _fill_chart(self):
        for _, text in enumerate(self.data_set.index):
            x = self.data_set.polarity.loc[text]
            y = self.data_set.subjectivity.loc[text]
            plot.scatter(x, y, color='Red')


class SentimentTable:
    template_file = 'assets/template.html'
    template_block = '<!-- template -->'

    def __init__(self, data_set):
        self.data_set = data_set

    def save(self, file_name='analysis.html'):
        template = open(self.template_file).read()
        rows = self._build_rows_html()
        html = template.replace(self.template_block, rows)
        self._save_file(file_name, html)

    def _build_rows_html(self):
        rows = self._get_rows()
        return '\n'.join(rows)

    def _get_rows(self):
        data = self.data_set.to_dict(orient='records')
        for row in data:
            yield self.row_template.format(
                tripadvisor_id=row['id'], text=row['text'], rating=row['rating'], subjectivity=round(row['subjectivity'], 2),
                polarity=round(row['polarity'], 2), color=self._get_css_color(row['polarity'])
            )

    @property
    def row_template(self):
        return ('<tr style="background-color: rgba({color});">'
                '<td>{tripadvisor_id}</td>'
                '<td>{text}</td>'
                '<td>{rating}</td>'
                '<td>{subjectivity}</td'
                '><td>{polarity}</td>'
                '</tr>')

    def _get_css_color(self, polarity):
        ratio = str(self._get_polarity_ratio(polarity))
        if polarity >= 0:
            color = ('0', '255', '0', ratio)
        else:
            color = ('255', '0', '0', ratio)
        return ', '.join(color)

    @staticmethod
    def _get_polarity_ratio(polarity):
        return round(abs(polarity) / 1.0, 2)

    @staticmethod
    def _save_file(file_name, html):
        new_file = open(file_name, 'w')
        new_file.write(html)
        new_file.close()
