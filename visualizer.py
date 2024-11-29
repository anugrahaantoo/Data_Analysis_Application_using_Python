import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot_histogram(data, title, xlabel, ylabel):
        labels, values = zip(*data.items())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
