#!/bin/bash
# ==============================================================================
# PCUtil Native Linux Deployment Script
# Description: Automates compilation, installs system files, and configures
#             PolicyKit for safe root execution under a graphical environment.
# Run with: sudo bash install.sh
# ==============================================================================

# Strict enforcement: Must be run with administrator/root privileges
if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: Please run this installation script using sudo."
  exit 1
fi

echo "=================================================================="
echo "🚀 Starting PCUtil Native Linux Desktop Deployment..."
echo "=================================================================="

# 1. Verification and Setup of Dependencies
echo "📦 Step 1: Verification of software compilation environment..."
if ! command -v pip &> /dev/null; then
    echo "   - Installing Python package manager..."
    if command -v apt-get &> /dev/null; then apt-get install -y python3-pip;
    elif command -v pacman &> /dev/null; then pacman -S --noconfirm python-pip;
    fi
fi

# Ensure mandatory framework dependencies are ready
pip install pyinstaller pyqt6 --quiet 2>/dev/null

# Make sure the core bash script is given appropriate permissions before packaging
chmod +x core_engine.sh

# 2. Binary Compilation Layer
echo "⚙️  Step 2: Compiling assets into a standalone binary..."
pyinstaller --onefile --windowed --add-data "core_engine.sh:." app.py --name pcutil --clean

if [ ! -f "dist/pcutil" ]; then
    echo "❌ Error: Compilation failed. Check your app.py syntax logs."
    exit 1
fi

# 3. System Binary Placement
echo "📂 Step 3: Installing system binaries..."
cp dist/pcutil /usr/local/bin/pcutil
chmod 755 /usr/local/bin/pcutil

# 4. App Launcher Desktop File Generation
echo "🖥️  Step 4: Generating desktop app menu shortcuts..."
cat <<EOF > /usr/share/applications/pcutil.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=PCUtil
Comment=Universal CPU Overclocking, Monitoring, and Tuning Utility
Exec=pkexec /usr/local/bin/pcutil
Icon=processor
Terminal=false
Categories=System;Settings;HardwareSettings;
Keywords=cpu;overclock;benchmark;tuner;amd;intel;pcutil;
StartupNotify=true
EOF

chmod 644 /usr/share/applications/pcutil.desktop

# 5. Security & PolicyKit Authentication Layer
echo "🔐 Step 5: Provisioning PolicyKit structural elevation tokens..."
cat <<EOF > /usr/share/polkit-1/actions/org.pcutil.pkexec.policy
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://freedesktop.org">
<policyconfig>
  <action id="org.pcutil.pkexec">
    <description>Run PCUtil with system privileges</description>
    <message>Authentication is required to allow PCUtil to manipulate hardware registers and system voltages.</message>
    <defaults>
      <allow_any>auth_admin</allow_any>
      <allow_inactive>auth_admin</allow_inactive>
      <allow_active>auth_admin</allow_active>
    </defaults>
    <annotate key="org.freedesktop.policykit.exec.path">/usr/local/bin/pcutil</annotate>
    <annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>
  </action>
</policyconfig>
EOF

chmod 644 /usr/share/polkit-1/actions/org.pcutil.pkexec.policy

# 6. Database and Menu Refresh System
echo "🔄 Step 6: Reloading global application registries..."
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/
fi

echo "=================================================================="
echo "✅ Deployment Successful!"
echo "🎉 You can now launch 'PCUtil' straight from your system app menu."
echo "=================================================================="
