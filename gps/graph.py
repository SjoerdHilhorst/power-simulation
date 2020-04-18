from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        self.app = QtWidgets.QApplication(sys.argv)
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ap_graph = pg.PlotWidget()
        self.setCentralWidget(self.ap_graph)
        self.ap_graph.setTitle("active power")


        #self.soc_graph = pg.PlotWidget()
        #self.setCentralWidget(self.soc_graph)

        self.api = []
        self.apo = []
        self.t = []

        pen = pg.mkPen(color=(255, 2, 0))
        self.api_plot = self.ap_graph.plot(self.t, self.api, name="active_power_in", pen=(255, 0, 0))
        self.apo_plot = self.ap_graph.plot(self.t, self.apo, "active_power_out", pen=(0, 255, 0))
        self.timer = QtCore.QTimer()
        self.show()


    def update_plot_data(self):

        self.api_plot.setData(self.t, self.api, pen=(255, 0, 0))  # Update the data.
        self.apo_plot.setData(self.t, self.apo, pen=(0, 255, 0))

    def run(self):
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        sys.exit(self.app.exec_())






