from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QFileDialog
from PyQt6.QtGui import QIcon
from logic.execution import ExecuteThread
from logic.plotting import PlotWindow
from logic.popups import Popup, LoadingPopup
from util.custom_widgets import CustomButton, CustomLabel, CustomInputBox

# Main Application Window
class SimulationApp(QMainWindow):
    """
    Main Window of the Application
    - Select an executable created from the OpenModelica model
    - Provide start and stop time for the simulation
    - Execute the simulation
    - If executed successfully, plot the simulation results
    """
    def __init__(self):
        super().__init__()
        self.plot_window = None      # To hold the Plot Window
        self.stop_time_input = None  # To hold stop time
        self.start_time_input = None # To hold start time
        self.browse_label = None     # To hold browse button
        self.plot_button = None      # To hold simulation plot button
        self.grid_layout = None      # To hold layout
        self.loading = None  # To hold loading popup while execution in process
        self.executable_file_path = None  # To hold selected executable path

        # Window configuration
        self.setWindowTitle("Simulate Model")
        self.setWindowIcon(QIcon("./resources/logo.png"))
        min_width, min_height = 500, 400
        self.setMinimumSize(500, 400)
        screen_geometry = self.screen().availableGeometry()
        # Set the window at the Center of screen
        self.setGeometry(
            screen_geometry.width() // 2 - min_width // 2,
            screen_geometry.height() // 2 - min_height // 2,
            500,
            400
        )
        # Maximized at start
        self.showMaximized()
        # Charcoal Black background
        self.setStyleSheet("background-color: #1a1a1a;")
        # Initialize UI Components
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface like buttons, labels, input boxes etc.
        """
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout(central_widget)
        self.grid_layout.setSpacing(10)

        # Button to plot simulation variables
        self.plot_button = CustomButton(
            "PLOT SIMULATION",
            "./resources/default_plot_icon.png",
            "./resources/hover_plot_icon.png"
        )
        self.plot_button.setFixedWidth(300)
        self.plot_button.clicked.connect(self.plot_model)
        self.plot_button.setFocusPolicy(Qt.FocusPolicy.TabFocus)

        # Button & Label to navigate and select the executable file
        browse_button = CustomButton(
            "BROWSE",
            "./resources/default_open_icon.png",
            "./resources/hover_open_icon.png"
        )
        browse_button.setFixedWidth(150)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        # Initially it's label has nothing to show up
        self.browse_label = CustomLabel("")
        self.browse_label.setStyleSheet(
            """
                QLabel {
                    font-size: 13px;
                    font-style: italic;
                    font-weight: normal;
                    color: #ffffff;
                    font-family: Calibri;
                }
            """
        )
        self.grid_layout.addWidget(
            browse_button,
            1,
            0,
            alignment = Qt.AlignmentFlag.AlignRight
        )
        self.grid_layout.addWidget(
            self.browse_label,
            1,
            1,
            alignment = Qt.AlignmentFlag.AlignLeft
        )

        # Button and Label to take 'startTime' from user
        start_time_label = CustomLabel("START TIME")
        self.start_time_input = CustomInputBox()
        self.grid_layout.addWidget(
            start_time_label,
            2,
            0,
            alignment = Qt.AlignmentFlag.AlignRight
        )
        self.grid_layout.addWidget(
            self.start_time_input,
            2,
            1,
            alignment = Qt.AlignmentFlag.AlignLeft
        )
        self.start_time_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # To set focus on start_time when window opens initially
        self.start_time_input.setFocus()

        # Button and Label to take 'stopTime' from user
        stop_time_label = CustomLabel("STOP TIME")
        self.stop_time_input = CustomInputBox()
        self.grid_layout.addWidget(
            stop_time_label,
            3,
            0,
            alignment = Qt.AlignmentFlag.AlignRight
        )
        self.grid_layout.addWidget(
            self.stop_time_input,
            3,
            1,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Button to validate the inputs and execute model
        # to show the plot_simulation button
        execute_button = CustomButton(
            "EXECUTE MODEL",
            "./resources/default_exec_icon.png",
            "./resources/hover_exec_icon.png"
        )
        execute_button.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        execute_button.clicked.connect(self.execute_model)
        execute_button.setFixedWidth(300)
        self.grid_layout.addWidget(
            execute_button,
            4,
            0,
            1,
            2,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

    def show_plot_button(self):
        """
        To Display the Plot Simulation Button after the Simulation is
         executed successfully.
        """
        self.grid_layout.addWidget(
            self.plot_button,
            0,
            0,
            1,
            2,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

    def browse_file(self):
        """
        Open a file dialog to select the executable file created from
         the OpenModelica model.
        """
        self.executable_file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Executable Simulation (*.exe)"
        )
        if self.executable_file_path:
            # If something is selected show the file name on browse_label
            label = " ... /" + self.executable_file_path.split("/")[-1]
            self.browse_label.setText(label)

    def execute_model(self):
        """
        Button to execute the selected simulation with specified
        start and stop time.
        """
        if self.executable_file_path is not None:
            try:
                # Validate startTime and stopTime
                start_time = int(self.start_time_input.text().strip())
                stop_time = int(self.stop_time_input.text().strip())
                if 0 <= start_time < stop_time < 5:
                    # Validated successfully, execute the model in another Thread
                    execute_thread = ExecuteThread(
                        self.executable_file_path,
                        start_time, stop_time, self
                    )
                    execute_thread.finished.connect(self.trigger_finished)
                    self.loading = LoadingPopup()
                    execute_thread.start()

                # Cases of validation failed
                elif start_time < 0:
                    Popup("Error",
                          "Please enter a valid start time and stop time.\nStart Time >= 0",
                          "error"
                    )
                elif stop_time > 5:
                    Popup("Error",
                          "Please enter a valid start time and stop time.\nStop Time <= 5",
                          "error"
                    )
                elif stop_time <= start_time:
                    Popup("Error",
                          "Please enter a valid start time and stop time.\nStop Time > Start Time",
                          "error"
                    )
                else:
                    Popup("Error",
                          "Please enter a valid start time and stop time.\n0 <= Start Time < Stop Time < 5",
                          "error"
                    )
            except ValueError:
                # Handle non-numeric values as input
                Popup(
                    "Error",
                    "Please enter a valid start time and stop time.\nThey must an Integer",
                    "error"
                )
        else:
            # Warning if executed without selecting any executable
            Popup(
                "Warning",
                "Please select an executable created from the OpenModelica model",
                "warning"
            )

    def trigger_finished(self, log: str, message: object):
        """
        Triggered when the execution thread is finished.
        """
        self.loading.close()
        if log == "LOG_SUCCESS":
            # If successfully simulated, show plot_button and success message
            self.show_plot_button()
            Popup(
                "SUCCESS",
                str(message) + "\nOpen Plot to see the Simulation Plots",
                "success"
            )
        else:
            # Show error message
            Popup(
                "ERROR",
                "Please! select an appropriate exe\n" + str(message),
                "error"
            )

    def plot_model(self):
        """
        Open a plot window to visualize the simulation results.
        """
        self.plot_window = PlotWindow(self.executable_file_path)
        self.plot_window.show()
