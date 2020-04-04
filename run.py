import analysis


analyzer = analysis.SentimentAnalyzer()
data = analyzer.build_data_set('data/skalny.json')

plotter = analysis.SentimentPlotter(data)
plotter.draw('sentiment_skalny.png')

printer = analysis.SentimentPrinter(data)
printer.save()
