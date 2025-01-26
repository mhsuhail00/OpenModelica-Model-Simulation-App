import sys
import PyQt6.QtWidgets
from ui import SimulationApp

def main():
    """
    Main Entry Point of the Application.

    """
    # Create an instance of QApplication
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    # Create Main Application Window
    window = SimulationApp()
    window.show()
    # Start the application's event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
