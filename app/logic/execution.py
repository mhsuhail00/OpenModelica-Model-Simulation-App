import os
import subprocess
import time
from PyQt6.QtCore import QThread, pyqtSignal

# Thread to Execute the model exe in background
class ExecuteThread(QThread):
    # Signal emitted when Execution is finished
    finished = pyqtSignal(str, object)
    def __init__(self, file_path, start_time, stop_time, parent = None):
        """
            Initializes the ExecuteThread with the executable file path
             and time parameters.
            :param file_path: Path to the executable file to run.
            :param start_time: Start time for the execution.
            :param stop_time: Stop time for the execution.
            :param parent: Optional parent widget.
        """
        super().__init__(parent)
        # Initialize file path and dynamic execution parameters
        self.executable_file_path = file_path
        self.start_time = start_time
        self.stop_time = stop_time

    def run(self):
        """
            Executes the model executable in the background.
            Emits a signal when the execution is finished,
            passing the first word of the output log and the full output.
        """
        # To suppress the CMD window
        command = [
            self.executable_file_path,
            f"-override=startTime={self.start_time},"
            f"stopTime={self.stop_time},"
            f"stepSize=0.002,"
            f"outputFormat=csv"
        ]
        # Execute exe in background
        execute = subprocess.run(
            command,
            cwd = os.path.dirname(self.executable_file_path),
            capture_output = True,
            text = True,
            creationflags = subprocess.CREATE_NO_WINDOW
        )
        # Just meant to show the animation atleast 1 sec
        time.sleep(1)
        # To Extract the Message log Title
        log = execute.stdout.split(" ")[0]
        # Signal the finish of execution
        self.finished.emit(log, execute.stdout.strip())
