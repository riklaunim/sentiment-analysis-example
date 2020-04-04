from libraries import analysis
from libraries import visualisation

analyzer = analysis.SentimentAnalyzer()
example_data = ['skalny', 'bania', 'qhotel']

for data_set_name in example_data:
    data_set = analyzer.build_data_set(f'data/{data_set_name}.json')

    plotter = visualisation.SentimentPlotter(data_set)
    plotter.draw(f'results/{data_set_name}/sentiment.png')

    printer = visualisation.SentimentTable(data_set)
    printer.save(f'results/{data_set_name}/analysis.html')
