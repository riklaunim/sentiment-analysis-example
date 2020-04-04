from libraries import analysis
from libraries import visualisation

analyzer = analysis.SentimentAnalyzer()
data = analyzer.build_data_set('data/skalny.json')

plotter = visualisation.SentimentPlotter(data)
plotter.draw('sentiment_skalny.png')

printer = visualisation.SentimentPrinter(data)
printer.save()
