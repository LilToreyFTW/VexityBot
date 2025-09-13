#!/usr/bin/env python3
"""
VexityBot Setup Script
Complete installation and configuration
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "data",
        "config",
        "backups",
        "temp",
        "dist",
        "build"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

def install_dependencies():
    """Install all required dependencies"""
    print("Installing Python dependencies...")
    
    dependencies = [
        "tkinter",
        "asyncio",
        "threading",
        "socket",
        "ssl",
        "json",
        "hashlib",
        "hmac",
        "base64",
        "zlib",
        "sqlite3",
        "requests",
        "scapy",
        "nmap",
        "cryptography",
        "dnspython",
        "concurrent.futures",
        "dataclasses",
        "enum34",
        "typing",
        "logging",
        "random",
        "string",
        "time",
        "datetime",
        "os",
        "sys",
        "pathlib",
        "pyinstaller"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"Installed: {dep}")
        except subprocess.CalledProcessError:
            print(f"Failed to install: {dep}")

def create_config_files():
    """Create configuration files"""
    
    # Main config
    config_content = '''
[VexityBot]
version = 2.0.0
vps_ip = 191.96.152.162
vps_port = 8080
encryption_key = VexityBot2024SecretKey
max_bots = 23
log_level = INFO

[Database]
type = sqlite
file = data/vexitybot.db
backup_interval = 3600

[Network]
timeout = 30
retry_count = 3
heartbeat_interval = 30

[Security]
encryption_enabled = true
ssl_enabled = true
signature_verification = true
'''
    
    with open('config/vexitybot.ini', 'w') as f:
        f.write(config_content)
    
    print("Created config/vexitybot.ini")
    
    # Bot configurations
    bot_configs = [
        ("AlphaBot", "Nuclear Warfare", 8081, "NUCLEAR_WARFARE"),
        ("BetaBot", "Cyber Warfare", 8082, "CYBER_WARFARE"),
        ("GammaBot", "Stealth Operations", 8083, "STEALTH_OPS"),
        ("DeltaBot", "EMP Warfare", 8084, "EMP_WARFARE"),
        ("EpsilonBot", "Biological Warfare", 8085, "BIO_WARFARE"),
        ("ZetaBot", "Gravity Control", 8086, "GRAVITY_CONTROL"),
        ("EtaBot", "Thermal Annihilation", 8087, "THERMAL_ANNIHILATION"),
        ("ThetaBot", "Cryogenic Freeze", 8088, "CRYOGENIC_FREEZE"),
        ("IotaBot", "Quantum Entanglement", 8089, "QUANTUM_ENTANGLEMENT"),
        ("KappaBot", "Dimensional Portal", 8090, "DIMENSIONAL_PORTAL"),
        ("LambdaBot", "Neural Network", 8091, "NEURAL_NETWORK"),
        ("MuBot", "Molecular Disassembly", 8092, "MOLECULAR_DISASSEMBLY"),
        ("NuBot", "Sound Wave Devastation", 8093, "SOUND_WAVE_DEVASTATION"),
        ("XiBot", "Light Manipulation", 8094, "LIGHT_MANIPULATION"),
        ("OmicronBot", "Dark Matter Control", 8095, "DARK_MATTER_CONTROL"),
        ("PiBot", "Mathematical Chaos", 8096, "MATHEMATICAL_CHAOS"),
        ("RhoBot", "Chemical Reactions", 8097, "CHEMICAL_REACTIONS"),
        ("SigmaBot", "Magnetic Fields", 8098, "MAGNETIC_FIELDS"),
        ("TauBot", "Time Manipulation", 8099, "TIME_MANIPULATION"),
        ("UpsilonBot", "Space-Time Fabric", 8100, "SPACE_TIME_FABRIC"),
        ("PhiBot", "Consciousness Control", 8101, "CONSCIOUSNESS_CONTROL"),
        ("ChiBot", "Energy Vortex", 8102, "ENERGY_VORTEX"),
        ("PsiBot", "Psychic Warfare", 8103, "PSYCHIC_WARFARE")
    ]
    
    for name, specialty, port, attack_type in bot_configs:
        bot_config = f'''
[{name}]
name = {name}
specialty = {specialty}
port = {port}
attack_type = {attack_type}
max_requests_per_second = 1000
max_threads = 10
auto_restart = true
encryption_enabled = true
'''
        
        with open(f'config/{name.lower()}.ini', 'w') as f:
            f.write(bot_config)
    
    print("Created bot configuration files")

def create_launcher():
    """Create launcher script"""
    launcher_content = '''
@echo off
title VexityBot Launcher
color 0A

echo.
echo  ██╗   ██╗███████╗██╗  ██╗██╗████████╗██╗   ██╗██████╗  ██████╗ ████████╗
echo  ██║   ██║██╔════╝╚██╗██╔╝██║╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
echo  ██║   ██║█████╗   ╚███╔╝ ██║   ██║    ╚████╔╝ ██████╔╝██║   ██║   ██║   
echo  ╚██╗ ██╔╝██╔══╝   ██╔██╗ ██║   ██║     ╚██╔╝  ██╔══██╗██║   ██║   ██║   
echo   ╚████╔╝ ███████╗██╔╝ ██╗██║   ██║      ██║   ██████╔╝╚██████╔╝   ██║   
echo    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ╚═════╝  ╚═════╝    ╚═╝   
echo.
echo                    Advanced Bot Management System v2.0.0
echo.
echo  [1] Start VexityBot GUI
echo  [2] Start Command Line Interface
echo  [3] Build Executable
echo  [4] Install Dependencies
echo  [5] Exit
echo.

set /p choice="Select option (1-5): "

if "%choice%"=="1" (
    echo Starting VexityBot GUI...
    python main.py
) else if "%choice%"=="2" (
    echo Starting Command Line Interface...
    python VexityBotCore.py
) else if "%choice%"=="3" (
    echo Building executable...
    python build_exe.py
) else if "%choice%"=="4" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else if "%choice%"=="5" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice!
    pause
    goto :eof
)

pause
'''
    
    with open('launcher.bat', 'w') as f:
        f.write(launcher_content)
    
    print("Created launcher.bat")

def create_desktop_shortcut():
    """Create desktop shortcut"""
    shortcut_content = '''
[InternetShortcut]
URL=file:///C:/VexityBot/VexityBot.exe
IconFile=C:/VexityBot/VexityBot.exe
IconIndex=0
'''
    
    with open('VexityBot.url', 'w') as f:
        f.write(shortcut_content)
    
    print("Created VexityBot.url (desktop shortcut)")

def main():
    """Main setup process"""
    print("VexityBot Setup Script")
    print("=====================")
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Create config files
    create_config_files()
    
    # Create launcher
    create_launcher()
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\nSetup completed successfully!")
    print("\nFiles created:")
    print("- logs/ (log files)")
    print("- data/ (database files)")
    print("- config/ (configuration files)")
    print("- launcher.bat (main launcher)")
    print("- VexityBot.url (desktop shortcut)")
    
    print("\nTo start VexityBot:")
    print("1. Run launcher.bat")
    print("2. Select option 1 for GUI")
    
    print("\nTo build executable:")
    print("1. Run launcher.bat")
    print("2. Select option 3")

if __name__ == "__main__":
    main()
