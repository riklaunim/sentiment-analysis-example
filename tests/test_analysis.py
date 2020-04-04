from unittest import mock

from libraries import analysis


class TestSentimentAnalyzer:
    def test_if_data_set_is_returned(self):
        analyzer = analysis.SentimentAnalyzer()
        result = analyzer.build_data_set('tests/test_data.json')

        expected = [
            {
                'id': '122566874',
                'text': 'I liked the music and the view was relaxing.',
                'rating': 4,
                'polarity': 0.6,
                'subjectivity': 0.8,
            },
            {
                'id': '122566875',
                'text': 'Rooms of high standard with good service and good staff. Excellent restaurant.',
                'rating': 3,
                'polarity': 0.512,
                'subjectivity': 0.548,
            },
        ]
        assert result.to_dict(orient='records') == expected

    @mock.patch('libraries.analysis.DataFrameFactory')
    def test_if_data_frame_factory_is_called(self, frame_factory):
        analyzer = analysis.SentimentAnalyzer()
        analyzer._get_data_frame('path/to/file.json')

        assert frame_factory.called
        calls = frame_factory.call_args_list
        assert calls[0].args[0] == 'path/to/file.json'

    def test_if_polarity_is_high_for_positive_phrase(self):
        analyzer = analysis.SentimentAnalyzer()
        result = analyzer._get_polarity('This is very good')
        assert round(result, 2) == 0.91

    def test_if_polarity_is_low_for_negative_phrase(self):
        analyzer = analysis.SentimentAnalyzer()
        result = analyzer._get_polarity('This is very bad')
        assert round(result, 2) == -0.91

    def test_if_subjectivity_is_low_for_objective_phrase(self):
        analyzer = analysis.SentimentAnalyzer()
        result = analyzer._get_subjectivity('Tom is a professional singer. Table was well made and rock solid.')
        assert round(result, 2) == 0.1

    def test_if_subjectivity_is_high_for_subjective_phrase(self):
        analyzer = analysis.SentimentAnalyzer()
        result = analyzer._get_subjectivity('I liked the concert, the music was very pleasing, I like the food')
        assert round(result, 2) == 0.55


class TestDataFrameFactory:
    def test_if_data_frame_is_returned(self):
        factory = analysis.DataFrameFactory('tests/test_data.json')
        result = factory.get_data_frame()

        expected = [
            {
                'id': '122566874',
                'text': 'I liked the music and the view was relaxing.',
                'rating': 4,
            },
            {
                'id': '122566875',
                'text': 'Rooms of high standard with good service and good staff. Excellent restaurant.',
                'rating': 3,
            },
        ]
        assert result.to_dict(orient='records') == expected

    @mock.patch('libraries.analysis.DataFrameFactory._get_raw_json')
    def test_if_raw_data_is_built_from_json(self, raw_json):
        raw_json.return_value = {"data": [
           {
              "type": "tripadvisor-reviews",
              "id": "122566874",
              "attributes": {
                 "reviewer-name": "Tomato",
                 "tripadvisor-id": 123,
                 "text": "I liked the music and the view was relaxing.",
                 "reviewed-at": "2012-01-01",
                 "rating": 4
              }
           },
        ]}

        factory = analysis.DataFrameFactory(None)
        result = list(factory._get_raw_data())

        expected = [
            analysis.TripAdvisorReview("122566874", "I liked the music and the view was relaxing.", 4),
        ]
        assert result == expected
