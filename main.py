import tkinter
import subprocess
import os
def findgpu():
  gpu_command = "wmic path win32_VideoController get name"
  gpu_name = subprocess.check_output(gpu_command, shell=True).decode().strip()
  if ("AMD" or "Radeon") in gpu_name:
    os.system('winget install "AMD Software" --source msstore')
    
