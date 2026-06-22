# PCUtil 💻⚡

An open-source, cross-vendor CPU optimization utility. Built for both Windows and Linux, PCUtil provides real-time telemetry, thread-pooled benchmarking, hardware driver updates, and low-level MSR tuning via a modern, dark-themed dashboard.

![License](https://shields.io)
![Platform](https://shields.io)

---

## ✨ Features

- ** Universal Hardware Detection**: Queries static metrics natively from the OS kernel—no manufacturer-locked software required.
- **⏱️ Isolated Thread-Pooled Benchmarker**: Mathematically stresses 100% of logical CPU threads using custom ALU/FPU calculations.
- **🔥 Core Thermal Watchdog**: Actively monitors package thermals during workloads and executes an emergency abort if temperatures breach 90°C.
- **🔧 Low-Level MSR Tuning Layout**: Contains interactive slider widgets designed to pass clock-multiplier configurations directly into CPU registers.
- **🔄 OS-Agnostic Driver Updates**: Communicates directly with upstream Windows Update APIs or native Linux package managers (`apt`, `pacman`, `dnf`) to keep processor microcode current.
- **🎨 Dark "Gamer" Dashboard**: Built with an optimized dark-mode stylesheet layout featuring cyber-neon teal highlights.

---

## 📋 System Requirements

PCUtil leverages low-level kernel abstractions (MSR manipulation) and heavy multi-threaded workloads. To prevent system instability, ensure your building or deployment machine meets the following criteria.

### 🪟 Windows Specifications

| Category | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Operating System** | Windows 10 (64-bit, Version 22H2) | Windows 11 (64-bit, Version 23H2 or newer) |
| **Execution Layer** | PowerShell 5.1 (Built-in) | PowerShell Core 7.x |
| **Developer Tools** | Python 3.10 + pip | Python 3.12 + pip |
| **Compilation Packages** | PyQt6 (v6.5+), PyInstaller (v6.0+) | PyQt6 (v6.7+), PyInstaller (v6.9+) |
| **User Privileges** | Local Administrator Account | Local Administrator Account |
| **System Security** | Core Isolation (HVCI) disabled *only* if flashing raw registers | Core Isolation / Driver Signature Enforcement active |

> ⚠️ **Windows Runtime Constraints:** The application **must** be compiled with the `--uac-admin` flag. If executed without full administrative rights, the `MSAcpi_ThermalZoneTemperature` WMI thermal zones and the Windows Update COM engine will immediately trigger a fatal `Access Denied` exception.

---

### 🐧 Linux Specifications

| Category | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Operating System** | Any stable 64-bit distro (Ubuntu 22.04+, Arch, Fedora 38+) | Current stable release (Ubuntu 24.04+, Arch Linux) |
| **Linux Kernel** | Kernel Version 5.15 or newer | Kernel Version 6.1 or newer (Optimized thread scheduling) |
| **Shell Environment** | GNU Bash 5.0+ | GNU Bash 5.2+ |
| **Required CLI Utilities** | `bc`, `grep`, `awk`, `sed` | `bc`, `xxd`, `dd`, `msr-tools` (for verified register writes) |
| **Security Subsystem** | PolicyKit (Polkit) | Polkit + `pkexec` package installed |
| **User Privileges** | User configured in the `sudoers` file | User configured in the `sudoers` file |

> ⚠️ **Linux Runtime Constraints:** PCUtil executes `modprobe msr` at startup. The host kernel must support model-specific registers (`CONFIG_X86_MSR=y` or `m`). Additionally, if hardware tracking paths like `k10temp` (AMD) or `coretemp` (Intel) are blacklisted or absent under `/sys/class/hwmon/`, the emergency thermal cutoff will fail gracefully to "Unknown" mode.

---

### 💻 Shared Hardware Minimums

The built-in benchmarker sets the processor load to 100%. To prevent hard lockups, the machine must meet these minimums:

* **Processor:** x86_64 Architecture (AMD Zen 1+ or Intel 6th Gen Skylake+). *ARM, Apple Silicon, and older 32-bit CPUs are explicitly unsupported.*
* **Cores:** Minimum **2 Physical Cores** (4 Logical Threads). Recommended **6+ Cores** so the OS interface remains responsive during stress loops.
* **Memory:** Minimum **4 GB RAM**. Recommended **8 GB+ RAM** to handle heavy mathematical allocations comfortably without disk thrashing.

---

## 🚀 Quick Start & Compilation

Clone the project repository and place `app.py` and the operating system's respective core engine file into the same directory before proceeding.

### For Windows Users

1. Install Python from [python.org](https://python.org) and ensure **"Add python.exe to PATH"** is checked.
2. Put `app.py`, `core_engine.ps1`, and `build.bat` in one folder.
3. Double-click **`build.bat`**.
4. Once finished, navigate to the newly created `.\dist\` folder and execute **`PCUtil.exe`** (accept the Windows UAC permission prompt).

### For Linux Users

Execute the automated `install.sh` deployment script with root rights to compile the source code, configure policy profiles, and create a system application menu launcher shortcut:

```bash
chmod +x install.sh
sudo ./install.sh
```

You can now locate and launch **PCUtil** directly from your desktop app manager panel.

---

## 🛠️ Troubleshooting

### [Linux] Error: Open /dev/cpu/0/msr failed: No such file or directory
The application is running without appropriate administrative credentials, or your distribution kernel hasn't instantiated the MSR framework module.
- Fix: Ensure you launch the application via `pkexec pcutil` or `sudo pcutil`. If the problem persists, manually load the driver block in your terminal: `sudo modprobe msr`.

### [Windows] WMI Thermal Zones return "N/A"
Certain motherboard manufacturers choose not to register their temperature metrics under Microsoft's generic ACPI WMI classes.
- Fix: Use vendor-specific monitoring tools, or utilize an open-source driver layer (like `OpenHardwareMonitor` APIs) to grab individual core metrics.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
