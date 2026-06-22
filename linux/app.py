import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QListWidget, QStackedWidget, QLabel, 
                             QPushButton, QTextEdit, QSlider, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

def get_script_path():
    # Dynamically resolve file paths whether running raw or inside PyInstaller executable bundle
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'core_engine.sh')
    return os.path.abspath('core_engine.sh')

class BashWorker(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(['sudo', 'bash', '-c', self.command], 
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.output_signal.emit(output.strip())
        process.poll()

class UniversalCpuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal Hardware Tuner & Optimizer")
        self.setMinimumSize(900, 550)

        # Apply Gamer/RyzenMaster styling theme rules
        self.setStyleSheet("""
            QMainWindow { background-color: #0d0e11; }
            QWidget { background-color: #12131a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
            QLabel { background: transparent; }
            QListWidget { background-color: #090a0d; border-right: 2px solid #1f232b; }
            QListWidget::item { padding: 18px 15px; color: #94a3b8; border-left: 4px solid transparent; }
            QListWidget::item:hover { background-color: #1a1d24; color: #f8fafc; }
            QListWidget::item:selected { background-color: #121620; color: #00ffcc; font-weight: bold; border-left: 4px solid #00ffcc; }
            QTextEdit { background-color: #090a0d; border: 1px solid #1f232b; border-radius: 6px; padding: 10px; font-family: monospace; color: #38bdf8; }
            QSlider::groove:horizontal { height: 6px; background: #1f232b; border-radius: 3px; }
            QSlider::handle:horizontal { background: #00ffcc; width: 16px; margin-top: -5px; margin-bottom: -5px; border-radius: 8px; }
            QPushButton { background-color: #1e293b; color: #f8fafc; border: 1px solid #334155; border-radius: 6px; padding: 10px 20px; font-weight: bold; }
            QPushButton:hover { background-color: #00ffcc; color: #090a0d; border: 1px solid #00ffcc; }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.taskbar = QListWidget()
        self.taskbar.setFixedWidth(200)
        self.taskbar.addItems(["💻 Specifications", "⏱️ Benchmarking", "🔧 MSR Tuning", "🔄 Driver Updates"])
        main_layout.addWidget(self.taskbar)

        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        self.init_specs_page()
        self.init_benchmark_page()
        self.init_tuning_page()
        self.init_updates_page()

        self.taskbar.currentRowChanged.connect(self.pages.setCurrentIndex)

    def init_specs_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Hardware Diagnostics")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ffcc; margin-bottom: 10px;")
        self.specs_display = QTextEdit("Initialize scan to poll active system architecture values...")
        self.specs_display.setReadOnly(True)
        
        btn = QPushButton("Scan Hardware Profiles")
        cmd = f"source {get_script_path()} && echo 'Processor Model:' && get_cpu_name && echo '' && echo 'Core Execution Threads:' && get_core_count && echo '' && echo 'Current Thermal Status:' && get_cpu_temp"
        btn.clicked.connect(lambda: self.run_bash_cmd(cmd, self.specs_display))
        
        layout.addWidget(title)
        layout.addWidget(self.specs_display)
        layout.addWidget(btn)
        self.pages.addWidget(page)

    def init_benchmark_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("CPU Performance Benchmark")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ffcc; margin-bottom: 10px;")
        self.bench_display = QTextEdit("Ready to run execution math computation loops...")
        self.bench_display.setReadOnly(True)
        
        btn = QPushButton("Execute Stress Loop")
        cmd = f"source {get_script_path()} && run_benchmark"
        btn.clicked.connect(lambda: self.run_bash_cmd(cmd, self.bench_display))
        
        layout.addWidget(title)
        layout.addWidget(self.bench_display)
        layout.addWidget(btn)
        self.pages.addWidget(page)

    def init_tuning_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Low-Level MSR Overclocking Controls")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ffcc; margin-bottom: 15px;")
        layout.addWidget(title)

        grid = QGridLayout()
        self.multiplier_label = QLabel("CPU Target Multiplier: 36.00x (3600 MHz)")
        self.multiplier_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(60)
        self.slider.setValue(36)
        self.slider.valueChanged.connect(self.on_multiplier_changed)
        
        grid.addWidget(self.multiplier_label, 0, 0)
        grid.addWidget(self.slider, 1, 0)
        layout.addLayout(grid)

        self.tuning_log = QTextEdit("Hardware adjustment logs ready...")
        self.tuning_log.setReadOnly(True)
        layout.addWidget(self.tuning_log)

        apply_btn = QPushButton("Flash Registers (Write MSR)")
        apply_btn.clicked.connect(self.apply_hardware_tuning)
        layout.addWidget(apply_btn)
        self.pages.addWidget(page)

    def on_multiplier_changed(self, value):
        self.multiplier_label.setText(f"CPU Target Multiplier: {value}.00x ({value * 100} MHz)")

    def apply_hardware_tuning(self):
        target_val = self.slider.value()
        hex_value = hex(target_val << 8)
        cmd = f"source {get_script_path()} && write_msr 0 0x199 {hex_value}"
        self.run_bash_cmd(cmd, self.tuning_log)

    def init_updates_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Kernel & Microcode Driver Updates")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ffcc; margin-bottom: 10px;")
        self.update_display = QTextEdit("Ready to probe system distribution trees...")
        self.update_display.setReadOnly(True)
        
        btn = QPushButton("Fetch Updates via Package Manager")
        cmd = f"source {get_script_path()} && update_system_drivers"
        btn.clicked.connect(lambda: self.run_bash_cmd(cmd, self.update_display))
        
        layout.addWidget(title)
        layout.addWidget(self.update_display)
        layout.addWidget(btn)
        self.pages.addWidget(page)

    def run_bash_cmd(self, cmd, display_widget):
        display_widget.clear()
        self.worker = BashWorker(cmd)
        self.worker.output_signal.connect(lambda text: display_widget.append(text))
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversalCpuApp()
    window.show()
    sys.exit(app.exec())
