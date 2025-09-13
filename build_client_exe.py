#!/usr/bin/env python3

"""
Build Client EXE for ShadowStrike OSRS Bot Controller
Creates a standalone executable for remote bot control
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_client_exe():
    """Build the client EXE using PyInstaller"""
    print("🔨 Building ShadowStrike OSRS Bot Controller EXE...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Create build directory
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create single executable
        "--windowed",  # No console window
        "--name=ShadowStrike_Bot_Controller",
        "--icon=icon.ico",  # Add icon if available
        "--add-data=README.md;.",  # Include README
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.scrolledtext",
        "--hidden-import=socket",
        "--hidden-import=json",
        "--hidden-import=threading",
        "--hidden-import=time",
        "--hidden-import=logging",
        "--hidden-import=datetime",
        "Client_Bot_Controller.py"
    ]
    
    # Remove icon parameter if icon doesn't exist
    if not os.path.exists("icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
    
    # Remove README parameter if it doesn't exist
    if not os.path.exists("README.md"):
        cmd = [arg for arg in cmd if not arg.startswith("--add-data")]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ PyInstaller completed successfully")
        
        # Check if EXE was created
        exe_path = dist_dir / "ShadowStrike_Bot_Controller.exe"
        if exe_path.exists():
            print(f"✅ EXE created successfully: {exe_path}")
            print(f"📁 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Create deployment package
            create_deployment_package()
            
        else:
            print("❌ EXE not found in dist directory")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    return True

def create_deployment_package():
    """Create deployment package with instructions"""
    print("📦 Creating deployment package...")
    
    # Create deployment directory
    deploy_dir = Path("deployment")
    deploy_dir.mkdir(exist_ok=True)
    
    # Copy EXE
    exe_src = Path("dist/ShadowStrike_Bot_Controller.exe")
    exe_dst = deploy_dir / "ShadowStrike_Bot_Controller.exe"
    shutil.copy2(exe_src, exe_dst)
    
    # Create configuration file
    config_content = """# ShadowStrike OSRS Bot Controller Configuration
# Edit these settings before running the client

# VPS Connection Settings
VPS_IP=YOUR_VPS_IP_HERE
VPS_PORT=9999

# Bot Settings
AUTO_CONNECT=false
AUTO_START_BOT=false
UPDATE_INTERVAL=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=client_bot_controller.log
"""
    
    config_file = deploy_dir / "config.txt"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    # Create README
    readme_content = """# ShadowStrike OSRS Bot Controller

## Quick Start

1. **Configure VPS Connection:**
   - Edit `config.txt` and set your VPS IP address
   - Default port is 9999 (change if needed)

2. **Run the Client:**
   - Double-click `ShadowStrike_Bot_Controller.exe`
   - Click "Connect" to connect to your VPS
   - Use the control buttons to manage the bot

## Features

- 🚀 Start/Stop/Restart bot remotely
- 📊 Real-time status monitoring
- 📋 View bot logs
- 🔄 Automatic status updates
- 🎮 Full bot control from anywhere

## VPS Setup

Make sure your VPS is running the bot server:
```bash
python VPS_Bot_Server.py --host 0.0.0.0 --port 9999
```

## Troubleshooting

- **Connection Failed:** Check VPS IP and port settings
- **Bot Won't Start:** Ensure VPS has the bot files
- **No Status Updates:** Check network connection

## Support

For issues or questions, check the log files:
- `client_bot_controller.log` - Client logs
- `vps_bot_server.log` - VPS server logs
"""
    
    readme_file = deploy_dir / "README.txt"
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    # Create batch file for easy VPS setup
    vps_setup_content = """@echo off
echo Setting up VPS Bot Server...
echo.

REM Install Python dependencies
pip install -r requirements.txt

REM Start the VPS server
echo Starting VPS Bot Server...
python VPS_Bot_Server.py --host 0.0.0.0 --port 9999

pause
"""
    
    vps_setup_file = deploy_dir / "setup_vps_server.bat"
    with open(vps_setup_file, 'w') as f:
        f.write(vps_setup_content)
    
    # Create requirements file for VPS
    vps_requirements = """# VPS Bot Server Requirements
socket
json
threading
time
logging
datetime
queue
pickle
pathlib
"""
    
    requirements_file = deploy_dir / "requirements.txt"
    with open(requirements_file, 'w') as f:
        f.write(vps_requirements)
    
    print(f"✅ Deployment package created in: {deploy_dir}")
    print("📁 Package contents:")
    for file in deploy_dir.iterdir():
        print(f"   - {file.name}")

def create_vps_deployment_script():
    """Create VPS deployment script"""
    print("📝 Creating VPS deployment script...")
    
    vps_script = """#!/bin/bash
# VPS Bot Server Deployment Script

echo "🚀 Deploying ShadowStrike OSRS Bot Server on VPS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install required packages
pip3 install -r requirements.txt

# Create bot directory
mkdir -p ~/shadowstrike_bot
cd ~/shadowstrike_bot

# Download bot files (you'll need to upload these)
# wget https://your-server.com/ShadowStrike_OSRS_Bot.py
# wget https://your-server.com/VPS_Bot_Server.py

# Set permissions
chmod +x VPS_Bot_Server.py

# Create systemd service
sudo tee /etc/systemd/system/shadowstrike-bot.service > /dev/null <<EOF
[Unit]
Description=ShadowStrike OSRS Bot Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/shadowstrike_bot
ExecStart=/usr/bin/python3 VPS_Bot_Server.py --host 0.0.0.0 --port 9999
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable shadowstrike-bot
sudo systemctl start shadowstrike-bot

echo "✅ VPS Bot Server deployed successfully!"
echo "📊 Check status: sudo systemctl status shadowstrike-bot"
echo "📋 View logs: sudo journalctl -u shadowstrike-bot -f"
"""
    
    with open("deploy_vps.sh", 'w') as f:
        f.write(vps_script)
    
    # Make executable
    os.chmod("deploy_vps.sh", 0o755)
    
    print("✅ VPS deployment script created: deploy_vps.sh")

def main():
    """Main function"""
    print("🤖 ShadowStrike OSRS Bot Controller EXE Builder")
    print("=" * 50)
    
    # Build client EXE
    if build_client_exe():
        print("\n🎉 Client EXE built successfully!")
        
        # Create VPS deployment script
        create_vps_deployment_script()
        
        print("\n📋 Next Steps:")
        print("1. Upload VPS files to your VPS server")
        print("2. Run 'deploy_vps.sh' on VPS to set up the server")
        print("3. Distribute the client EXE to users")
        print("4. Users can connect and control the bot remotely")
        
    else:
        print("\n❌ Failed to build client EXE")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
