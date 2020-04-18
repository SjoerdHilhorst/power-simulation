from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
import sys


class Graph(pg.GraphicsWindow):

    def __init__(self, fields, *args, **kwargs):
        super().__init__(title="graph", *args, **kwargs)
        self.app = QtGui.QApplication(sys.argv)

        self.data = {}
        self.graphs = {}

        for field in fields:
            graph = self.addPlot(title=field)
            self.graphs[field] = graph.plot()
            if field == "soc":
                graph.setYRange(0,100)
            self.nextRow()

            self.data[field] = []

        self.timer = QtCore.QTimer()
        self.show()

    def update_plot_data(self):
        for key, graph in self.graphs.items():
            graph.setData(list(range(len(self.data[key]))), self.data[key], pen=(255,0,0))

    def run(self):
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        sys.exit(self.app.exec_())






