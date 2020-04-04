from unittest import mock

import pandas

from libraries import visualisation


class TestSentimentPlotter:
    @mock.patch('matplotlib.pyplot.savefig')
    def test_if_chart_is_drawn(self, savefig):
        data = pandas.DataFrame([], columns=[])
        plotter = visualisation.SentimentPlotter(data)
        plotter.draw()
        assert savefig.called

    @mock.patch('matplotlib.pyplot.scatter')
    def test_if_data_is_plotted(self, scatter):
        review = {
            'id': 123, 'text': 'zzz', 'rating': 5, 'polarity': 0.9, 'subjectivity': 0.2
        }
        data = pandas.DataFrame([review], columns=['id', 'text', 'rating', 'polarity', 'subjectivity'])

        plotter = visualisation.SentimentPlotter(data)
        plotter._fill_chart()

        call = scatter.call_args_list[0]
        assert call.args == (0.9, 0.2)


class TestSentimentTable:
    @mock.patch('libraries.visualisation.SentimentTable._save_file')
    def test_if_file_is_saved(self, save_file):
        review = {
            'id': 123, 'text': 'zzz', 'rating': 5, 'polarity': 0.9, 'subjectivity': 0.2
        }
        data = pandas.DataFrame([review], columns=['id', 'text', 'rating', 'polarity', 'subjectivity'])

        printer = visualisation.SentimentTable(data)
        printer.save()

        call = save_file.call_args_list[0]
        assert call.args[0] == 'analysis.html'
        assert '<tr><td>123</td><td>zzz</td><td>5</td><td>0.2</td><td>0.9</td></tr>' in call.args[1]
