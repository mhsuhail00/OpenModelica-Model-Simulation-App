from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel

# Customized Input Box Class
class CustomInputBox(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set PlaceHolder text and Set Start and Stop time Validators
        self.setPlaceholderText("Enter a Positive Integer")
        self.setValidator(QIntValidator(0, 4))
        # Style for Input Box
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
        # Fixed width for the default size
        self.setFixedWidth(150)

# Custom Label class
class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Style for Label
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

# Customised Button Class with Icon
class CustomButton(QPushButton):
    def __init__(self, text, default_icon_path, hover_icon_path, parent=None):
        """
            Initializes the CustomButton with text, default and hover icons.
            :param text: Text to display on the button.
            :param default_icon_path: Path to the default icon.
            :param hover_icon_path: Path to the hover icon.
            :param parent: Optional parent widget.
        """
        super().__init__(text, parent)
        # Remove default Focus Policies
        self.is_focused = False
        self.is_clicked = False
        # Set Hand Cursor when hovered on to the button
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # Style for Button
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
        # Set Global Variable for default and hover icon
        self.default_icon = QIcon(default_icon_path)
        self.hover_icon = QIcon(hover_icon_path)
        # Set default Icon on Button
        self.setIcon(self.default_icon)
        # Install an event filter to handle hover events
        self.installEventFilter(self)

    # Event filter to change the icon when hovering over the button
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Enter:
            self.setIcon(self.hover_icon)
        elif event.type() == QEvent.Type.Leave:
            if not self.is_focused:
                self.setIcon(self.default_icon)
        return super().eventFilter(source, event)

    # Handle mouse press event
    def mousePressEvent(self, event):
        self.is_clicked = True
        self.setIcon(self.default_icon)
        super().mousePressEvent(event)

    # Handle mouse release event
    def mouseReleaseEvent(self, event):
        if self.is_clicked:
            self.setIcon(self.hover_icon)
            self.is_clicked = False
        super().mouseReleaseEvent(event)

    # Handle focus-in event (when the button gains focus)
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

    # Handle focus-out event (when the button loses focus)
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

    # Handle space-bar press event, it is used to mimic click event
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.setIcon(self.default_icon)
            super().keyPressEvent(event)

    # Handle space-bar release event
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.setIcon(self.hover_icon)
            super().keyReleaseEvent(event)

