import sys
from PyQt6.QtWidgets import QApplication
from ui import SimulationApp

def main():
    """
    Main Entry Point of the Application.

    """
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    # Create Main Application Window
    window = SimulationApp()
    window.show()
    # Start the application's event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
