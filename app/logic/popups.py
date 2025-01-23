from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QIcon, QPixmap
from util.custom_widgets import CustomButton


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
