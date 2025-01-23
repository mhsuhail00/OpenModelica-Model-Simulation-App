import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QScrollArea
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from util.custom_widgets import CustomButton, CustomLabel

class PlotWindow(QMainWindow):
    def __init__(self, path:str):
        super().__init__()
        self.plotting_data = None
        self.grid_layout = None
        self.path = path
        self.setup_ui()
    def setup_ui(self):
        self.showMaximized()
        self.setWindowTitle("Simulation Plot")
        self.setWindowIcon(QIcon("./resources/logo.png"))
        self.setStyleSheet("background-color: #1a1a1a;")
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        central_widget = QWidget()
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
        self.grid_layout = QGridLayout(central_widget)
        self.grid_layout.setSpacing(10)

        self.path = self.path[:-4] + "_res.csv"
        self.plotting_data = pd.read_csv(self.path)

        for var in range(1, len(self.plotting_data.columns)):
            setattr(self, f'label_{var - 1}', CustomLabel(self.plotting_data.columns[var]))
            self.grid_layout.addWidget(getattr(self, f'label_{var - 1}'), var - 1, 0, Qt.AlignmentFlag.AlignRight)

            setattr(self, f'button_{var - 1}', CustomButton("SHOW", "./resources/default_show_icon.png", "./resources/hover_show_icon.png"))
            button = getattr(self, f'button_{var - 1}')
            button.setFixedHeight(30)
            button.clicked.connect(self.show_plot)
            button.setObjectName(f'{var}')
            self.grid_layout.addWidget(getattr(self, f'button_{var - 1}'), var - 1, 1, Qt.AlignmentFlag.AlignLeft)
    def show_plot(self):
        var = self.sender()
        x_label = self.plotting_data.columns[0]
        y_label = self.plotting_data.columns[int(var.objectName())]
        fig, pl = plt.subplots()
        pl.plot(self.plotting_data[x_label], self.plotting_data[y_label], label = y_label)
        pl.set_xlabel(x_label)
        pl.set_ylabel(y_label)
        pl.set_title(y_label + " vs " + x_label)
        pl.legend()
        fig.canvas.manager.set_window_title(f'Simulation Plot - {y_label}')
        plt.show()
