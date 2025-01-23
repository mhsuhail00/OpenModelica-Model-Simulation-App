import os
import subprocess
import time
from PyQt6.QtCore import QThread, pyqtSignal


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
