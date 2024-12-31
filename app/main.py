import os.path
import subprocess
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt, QEvent, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, QLineEdit, QLabel, QWidget, QPushButton,
                             QFileDialog, QDialog, QVBoxLayout, QScrollArea)
from PyQt6.QtGui import QIcon, QIntValidator, QPixmap


class SimulationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_window = None
        self.stop_time_input = None
        self.start_time_input = None
        self.browse_label = None
        self.plot_button = None
        self.grid_layout = None
        self.loading = None
        self.executable_file_path = None

        self.setWindowTitle("Simulate Model")
        self.setWindowIcon(QIcon("./resources/logo.png"))
        min_width, min_height = 500, 400
        self.setMinimumSize(500, 400)
        screen_geometry = self.screen().availableGeometry()
        self.setGeometry(
            screen_geometry.width() // 2 - min_width // 2,
            screen_geometry.height() // 2 - min_height // 2,
            500,
            400
        )
        self.showMaximized()
        self.setStyleSheet("background-color: #1a1a1a;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout(central_widget)
        self.grid_layout.setSpacing(10)

        self.plot_button = CustomButton("PLOT SIMULATION", "./resources/default_plot_icon.png", "./resources/hover_plot_icon.png")
        self.plot_button.setFixedWidth(300)
        self.plot_button.clicked.connect(self.plot_model)
        self.plot_button.setFocusPolicy(Qt.FocusPolicy.TabFocus)

        browse_button = CustomButton("BROWSE", "./resources/default_open_icon.png", "./resources/hover_open_icon.png")
        browse_button.setFixedWidth(150)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setFocusPolicy(Qt.FocusPolicy.TabFocus)
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
        self.grid_layout.addWidget(browse_button, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(self.browse_label, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        start_time_label = CustomLabel("START TIME")
        self.start_time_input = CustomInputBox()
        self.start_time_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.grid_layout.addWidget(start_time_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(self.start_time_input, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.start_time_input.setFocus()

        stop_time_label = CustomLabel("STOP TIME")
        self.stop_time_input = CustomInputBox()
        self.grid_layout.addWidget(stop_time_label, 3, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(self.stop_time_input, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        execute_button = CustomButton("EXECUTE MODEL", "./resources/default_exec_icon.png", "./resources/hover_exec_icon.png")
        execute_button.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        execute_button.clicked.connect(self.execute_model)
        execute_button.setFixedWidth(300)
        self.grid_layout.addWidget(execute_button, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

    def show_plot_button(self):
        self.grid_layout.addWidget(self.plot_button, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

    def browse_file(self):
        self.executable_file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Executable Simulation (*.exe)")
        if self.executable_file_path:
            label = " ... /" + self.executable_file_path.split("/")[-1]
            self.browse_label.setText(label)

    def execute_model(self):
        if self.executable_file_path is not None:
            try:
                start_time = int(self.start_time_input.text().strip())
                stop_time = int(self.stop_time_input.text().strip())
                if 0 <= start_time < stop_time < 5:
                    execute_thread = ExecuteThread(self.executable_file_path, start_time, stop_time, self)
                    execute_thread.finished.connect(self.trigger_finished)
                    self.loading = LoadingPopup()
                    execute_thread.start()

                elif start_time < 0:
                    Popup("Error",
                          "Please enter a valid start time and stop time.\nStart Time >= 0",
                          "error")
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
                          "error")
            except ValueError:
                    Popup("Error", "Please enter a valid start time and stop time.\nThey must an Integer", "error")
        else:
            Popup("Warning", "Please select an executable created from the OpenModelica model", "warning")

    def trigger_finished(self, log:str, message:object):
        self.loading.close()
        if log == "LOG_SUCCESS":
            self.show_plot_button()
            Popup("SUCCESS", message + "\nOpen Plot to see the Simualtion Plots", "success")
        else:
            Popup("ERROR", message, "error")

    def plot_model(self):
        self.plot_window = PlotWindow(self.executable_file_path)
        self.plot_window.show()


class ExecuteThread(QThread):
    finished = pyqtSignal(str, object)
    def __init__(self, file_path, start_time, stop_time, parent=None):
        super().__init__(parent)
        self.executable_file_path = file_path
        self.start_time = start_time
        self.stop_time = stop_time

    def run(self):
        command = [self.executable_file_path, f"-override=startTime={self.start_time},stopTime={self.stop_time},stepSize=0.002,outputFormat=csv"]
        execute = subprocess.run(command, cwd=os.path.dirname(self.executable_file_path), capture_output=True, text=True)
        time.sleep(1)
        log = execute.stdout.split(" ")[0]
        self.finished.emit(log, execute.stdout.strip())

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

class CustomInputBox(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Enter a Positive Integer")
        self.setValidator(QIntValidator(0, 4))
        self.setStyleSheet(
            """
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    height: 25px;
                    border: 1.5px solid #333333;
                    border-radius: 3px;
                    padding: 0 8px;
                }
                QLineEdit:focus {
                    border: 1.5px solid #00bcd4;
                }
            """
        )
        self.setFixedWidth(150)

class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    font-family: Calibri;
                    color: #ffffff;
                }
            """
        )

class CustomButton(QPushButton):
    def __init__(self, text, default_icon_path, hover_icon_path, parent=None):
        super().__init__(text, parent)
        self.is_focused = False
        self.is_clicked = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            """
                QPushButton {
                    background-color: #00bcd4;
                    color: #ffffff;
                    font-family: Calibri;
                    font-size: 16px;
                    font-weight: bold;
                    height: 28px;
                    border-radius: 3px;
                    border: 1.5px solid #00bcd4;
                    padding: 0 5px;
                }
                QPushButton:hover {
                    background-color: #1a1a1a;
                    color: #00bcd4;
                    border: 1.5px solid #ffffff;
                }
                QPushButton:pressed {
                    background-color: #00bcd4;
                    color: #ffffff;
                    border: 1.5px solid #00bcd4;
                }
            """
        )
        self.default_icon = QIcon(default_icon_path)
        self.hover_icon = QIcon(hover_icon_path)
        self.setIcon(self.default_icon)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Enter:
            self.setIcon(self.hover_icon)
        elif event.type() == QEvent.Type.Leave:
            if not self.is_focused:
                self.setIcon(self.default_icon)
        return super().eventFilter(source, event)

    def mousePressEvent(self, event):
        self.is_clicked = True
        self.setIcon(self.default_icon)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_clicked:
            self.setIcon(self.hover_icon)
            self.is_clicked = False
        super().mouseReleaseEvent(event)

    def focusInEvent(self, event):
        self.setIcon(self.hover_icon)
        self.is_focused = True
        self.setStyleSheet(
            """
            QPushButton {
                    background-color: #1a1a1a;
                    color: #00bcd4;
                    font-family: Calibri;
                    font-size: 16px;
                    font-weight: bold;
                    height: 28px;
                    border-radius: 3px;
                    border: 1.5px solid #00bcd4;
                    padding: 0 5px;
                }
                QPushButton:focus{
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #1a1a1a;
                    color: #00bcd4;
                    border: 1.5px solid #ffffff;
                }
                QPushButton:pressed {
                    background-color: #00bcd4;
                    color: #ffffff;
                    border: 1.5px solid #00bcd4;
                }
            """
        )
        super().focusInEvent(event)
    def focusOutEvent(self, event):
        self.setIcon(self.default_icon)
        self.is_focused = False
        self.setStyleSheet(
            """
                 QPushButton {
                    background-color: #00bcd4;
                    color: #ffffff;
                    font-family: Calibri;
                    font-size: 16px;
                    font-weight: bold;
                    height: 28px;
                    border-radius: 3px;
                    border: 1.5px solid #00bcd4;
                    padding: 0 5px;
                }
                QPushButton:hover {
                    background-color: #1a1a1a;
                    color: #00bcd4;
                    border: 1.5px solid #ffffff;
                }
                QPushButton:pressed {
                    background-color: #00bcd4;
                    color: #ffffff;
                    border: 1.5px solid #00bcd4;
                }
            """
        )
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.setIcon(self.default_icon)
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.setIcon(self.hover_icon)
            super().keyReleaseEvent(event)

class Popup(QDialog):
    def __init__(self, title, message, type:str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./resources/logo.png"))
        self.setStyleSheet(
            """
                QDialog {
                    background-color: #1a1a1a;
                    color: #ffffff;
                    font-family: Calibri;
                }
            """
        )
        layout = QGridLayout(self)
        message_label = QLabel(message)
        message_label.setStyleSheet(
            """
            QLabel {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: Calibri;
                font-size: 14px;
            }
            """
        )
        layout.addWidget(message_label, 0, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

        if type == "warning":
            path = "./resources/warning_icon.png"
        elif type == "error":
            path = "./resources/error_icon.png"
        elif type == "info":
            path = "./resources/info_icon.png"
        elif type == "success":
            path = "./resources/success_icon.png"
        else:
            path = "./resources/info_icon.png"

        icon_pixmap = QPixmap(path).scaled(37, 37, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label = QLabel()
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter)

        ok_button = CustomButton("OK", "./resources/default_ok_icon.png", "./resources/hover_ok_icon.png")
        ok_button.setFixedWidth(100)
        ok_button.setFixedHeight(30)
        ok_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(ok_button, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)
        ok_button.clicked.connect(self.close)
        self.exec()

class LoadingPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setWindowIcon(QIcon('./Resources/logo.png'))
        width, height = self.screen().availableGeometry().width() * 25 // 100, self.screen().availableGeometry().height() * 23 // 100
        left, top = width * 3 // 2, height * 77 // 46
        self.setGeometry(left, top, width, height)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        self.loading_label = QLabel("Execution in Progress.\n Please wait    ", self)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(
            """
                QLabel {
                    font-family: Monospace;
                    font-size: 16px;
                    color: #00bcd4;
                }
            """
        )
        layout.addWidget(self.loading_label)

        self.show_dot = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_message)
        # Blinking Time
        self.timer.start(1000)
        self.show()

    def update_message(self):
        if self.show_dot == 0:
            self.loading_label.setText(f"Execution in Progress.\n Please wait .  ")
            self.show_dot = 1
        elif self.show_dot == 1:
            self.loading_label.setText(f"Execution in Progress.\n Please wait .. ")
            self.show_dot = 2
        elif self.show_dot == 2:
            self.loading_label.setText(f"Execution in Progress.\n Please wait ...")
            self.show_dot = 3
        elif self.show_dot == 3:
            self.loading_label.setText(f"Execution in Progress.\n Please wait    ")
            self.show_dot = 0

def main():
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
