import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


class Graph:

    def __init__(self, fields):
        style.use('ggplot')
        self.fig = plt.figure()
        self.data = {'time': 0}
        self.graphs = {}

        idx = 1
        for field in fields:
            subplot = self.fig.add_subplot(len(fields), 1, idx)
            subplot.set_title(field, fontsize=10)
            self.graphs[field] = subplot
            self.data[field] = []
            idx += 1

    def animate(self, i):
        for key, graph in self.graphs.items():
            graph.plot(list(range(self.data['time'])), self.data[key], color='green', linewidth=0.4)

    def run(self):
        self.anim = animation.FuncAnimation(self.fig, self.animate)
        plt.show()
