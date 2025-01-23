from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel

# Customized input box
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

