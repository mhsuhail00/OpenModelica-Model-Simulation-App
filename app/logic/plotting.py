import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QScrollArea
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from util.custom_widgets import CustomButton, CustomLabel

class PlotWindow(QMainWindow):
    def __init__(self, path:str):
        """
            Initializes the PlotWindow with the given CSV file path.
            :param path: Path to the CSV file containing simulation data.
        """
        super().__init__()
        # Initialize global variables
        self.plotting_data = None
        self.grid_layout = None
        self.path = path
        # Set up the user interface
        self.setup_ui()
    def setup_ui(self):
        """
            Sets up the user interface, including the layout, scroll area,
            and dynamic creation of labels and buttons for plotting.
        """
        # Maximize window Initially
        self.showMaximized()
        # Set basic properties
        self.setWindowTitle("Simulation Plot")
        self.setWindowIcon(QIcon("./resources/logo.png"))
        self.setStyleSheet("background-color: #1a1a1a;")
        # Set a scroll area to accommodate the dynamic content overflows
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        central_widget = QWidget()
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
        # Set up the grid layout for scrollable content
        self.grid_layout = QGridLayout(central_widget)
        self.grid_layout.setSpacing(10)
        # Adjust the file path to point to the result CSV file
        self.path = self.path[:-4] + "_res.csv"
        # Load the plotting data from the CSV file
        self.plotting_data = pd.read_csv(self.path)
        # Dynamically create labels and buttons for each column in the data
        for var in range(1, len(self.plotting_data.columns)):
            # Create a label for the variable (column)
            setattr(self, f'label_{var - 1}', CustomLabel(self.plotting_data.columns[var]))
            self.grid_layout.addWidget(getattr(self, f'label_{var - 1}'), var - 1, 0, Qt.AlignmentFlag.AlignRight)
            # Create a button to show the plot for the variable
            setattr(self, f'button_{var - 1}', CustomButton("SHOW", "./resources/default_show_icon.png", "./resources/hover_show_icon.png"))
            button = getattr(self, f'button_{var - 1}')
            button.setFixedHeight(30)
            button.clicked.connect(self.show_plot)
            button.setObjectName(f'{var}')
            self.grid_layout.addWidget(getattr(self, f'button_{var - 1}'), var - 1, 1, Qt.AlignmentFlag.AlignLeft)
    def show_plot(self):
        """
            Displays a plot for the selected variable (column) in the data.
            Triggered when a button is clicked.
        """
        # Get the button that triggered the event
        var = self.sender()
        # Retrieve the x-axis and y-axis labels from the data
        x_label = self.plotting_data.columns[0]
        y_label = self.plotting_data.columns[int(var.objectName())]
        # Create a new plot
        fig, pl = plt.subplots()
        pl.plot(self.plotting_data[x_label], self.plotting_data[y_label], label = y_label)
        # Set labels, title, and legend for the plot
        pl.set_xlabel(x_label)
        pl.set_ylabel(y_label)
        pl.set_title(y_label + " vs " + x_label)
        pl.legend()
        # Set the plot window title
        fig.canvas.manager.set_window_title(f'Simulation Plot - {y_label}')
        # Display the plot
        plt.show()
