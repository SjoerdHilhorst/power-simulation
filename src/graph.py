from PyQt5 import QtCore, QtGui
from PyQt5.Qt import QMutex
import pyqtgraph as pg
import sys


class Graph(pg.GraphicsWindow):

    def __init__(self, fields, *args, **kwargs):
        super().__init__(title="graph", *args, **kwargs)
        self.app = QtGui.QApplication(sys.argv)
        self.data = {'t': 0}
        self.graphs = {}

        for field in fields:
            graph = self.addPlot(title=field)
            self.graphs[field] = graph.plot()
            self.nextRow()
            self.data[field] = []

        self.mutex = QMutex()
        self.timer = QtCore.QTimer()
        self.show()
        self.t = 0

    def update_plot_data(self):
        self.mutex.lock()
        for key, graph in self.graphs.items():
            graph.setData(list(range(self.data['t'])), self.data[key], pen='g')
        self.mutex.unlock()

    def run(self):
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        sys.exit(self.app.exec_())






