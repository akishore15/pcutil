import sys
import os
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow # ... (Keep your structural UI elements from previous code)

def get_script_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'core_engine.ps1')
    return os.path.abspath('core_engine.ps1')

class PowerShellWorker(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        # Executes elevated script paths safely inside an un-restricted execution policy pipeline
        process = subprocess.Popen([
            'powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', self.command
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.output_signal.emit(output.strip())
        process.poll()

# Inside your GUI Page click events, replace command references like this:
# cmd = f". '{get_script_path()}'; Get-CpuName"
