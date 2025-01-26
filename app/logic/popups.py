from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QIcon, QPixmap
from util.custom_widgets import CustomButton

# Custom Dialog to create Popup's to show Messages
class Popup(QDialog):
    def __init__(self, title, message, type: str, parent = None):
        """
            Initializes the Popup dialog with a title, message, and type.
            :param title: Title of the popup window.
            :param message: Message to display in the popup.
            :param type: Type of message (warning, error, info, success).
            :param parent: Optional parent widget.
        """
        super().__init__(parent)
        # Set Window Title
        self.setWindowTitle(title)
        # Set Standard Icon of Window
        self.setWindowIcon(QIcon("./resources/logo.png"))
        # Set Style for Dialog
        self.setStyleSheet(
            """
                QDialog {
                    background-color: #1a1a1a;
                    color: #ffffff;
                    font-family: Calibri;
                }
            """
        )
        # Layout of Popup
        layout = QGridLayout(self)
        # Message Label
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
        layout.addWidget(
            message_label,
            0,
            1,
            alignment = Qt.AlignmentFlag.AlignVCenter
        )
        # Set the path of Icon based on the type of Message
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

        # Icon Label
        icon_pixmap = QPixmap(path).scaled(
            37,
            37,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        icon_label = QLabel()
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(
            icon_label,
            0,
            0,
            alignment = Qt.AlignmentFlag.AlignVCenter
        )

        # Ok Button of Dialog
        ok_button = CustomButton(
            "OK",
            "./resources/default_ok_icon.png",
            "./resources/hover_ok_icon.png"
        )
        ok_button.setFixedWidth(100)
        ok_button.setFixedHeight(30)
        ok_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(
            ok_button,
            1,
            0,
            1,
            2,
            alignment = Qt.AlignmentFlag.AlignRight
        )
        ok_button.clicked.connect(self.close)
        self.exec()

# Custom Dialog to be shown while the ExecuteThread is Running
class LoadingPopup(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        # Set Window Title
        self.setWindowTitle("Loading")
        # Set Window Icon
        self.setWindowIcon(QIcon('./Resources/logo.png'))
        # Set Window size and position
        width, height = (
            self.screen().availableGeometry().width() * 25 // 100,
            self.screen().availableGeometry().height() * 23 // 100
        )
        left, top = width * 3 // 2, height * 77 // 46
        self.setGeometry(left, top, width, height)
        # Popup cannot be closed by user
        self.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
        )
        # Styling the window
        self.setStyleSheet("background-color: #ffffff;")
        # Layout for loading Popup
        layout = QVBoxLayout(self)
        # Loading Message
        self.loading_label = QLabel(
            "Execution in Progress.\n Please wait    ",
            self
        )
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
        # Variable to keep track of the Animation
        self.show_dot = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_message)
        # Transition Time 1 sec
        self.timer.start(1000)
        self.show()

    # Update the Label forever the popup is showing
    def update_message(self):
        # Keep on increasing the '.' from 0 to 3 and repeat
        if self.show_dot == 0:
            self.loading_label.setText(
                f"Execution in Progress.\n Please wait .  "
            )
            self.show_dot = 1
        elif self.show_dot == 1:
            self.loading_label.setText(
                f"Execution in Progress.\n Please wait .. "
            )
            self.show_dot = 2
        elif self.show_dot == 2:
            self.loading_label.setText(
                f"Execution in Progress.\n Please wait ..."
            )
            self.show_dot = 3
        elif self.show_dot == 3:
            self.loading_label.setText(
                f"Execution in Progress.\n Please wait    "
            )
            self.show_dot = 0
