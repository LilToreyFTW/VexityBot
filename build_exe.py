#!/usr/bin/env python3
"""
VexityBot Executable Builder
Creates standalone executable with all components
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('main_gui.py', '.'),
        ('VexityBotCore.py', '.'),
        ('VexityBotNetworking.py', '.'),
        ('VexityBotJavaFX.java', '.'),
        ('VexityBotCpp.h', '.'),
        ('VexityBotCpp.cpp', '.'),
        ('VexityBotCSharp.cs', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'asyncio',
        'threading',
        'socket',
        'ssl',
        'json',
        'hashlib',
        'hmac',
        'base64',
        'zlib',
        'sqlite3',
        'requests',
        'scapy',
        'nmap',
        'cryptography',
        'dnspython',
        'concurrent.futures',
        'dataclasses',
        'typing',
        'logging',
        'random',
        'string',
        'time',
        'datetime',
        'os',
        'sys',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VexityBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('VexityBot.spec', 'w') as f:
        f.write(spec_content)
    
    print("PyInstaller spec file created")

def create_icon():
    """Create application icon"""
    # Create a simple icon file (placeholder)
    icon_content = '''
# This is a placeholder for the icon
# In a real implementation, you would use a proper .ico file
'''
    
    with open('icon.ico', 'w') as f:
        f.write(icon_content)
    
    print("Icon file created (placeholder)")

def build_executable():
    """Build the executable"""
    print("Building VexityBot executable...")
    
    try:
        # Run PyInstaller
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=VexityBot",
            "--add-data=main_gui.py;.",
            "--add-data=VexityBotCore.py;.",
            "--add-data=VexityBotNetworking.py;.",
            "--add-data=VexityBotJavaFX.java;.",
            "--add-data=VexityBotCpp.h;.",
            "--add-data=VexityBotCpp.cpp;.",
            "--add-data=VexityBotCSharp.cs;.",
            "--add-data=requirements.txt;.",
            "--hidden-import=tkinter",
            "--hidden-import=asyncio",
            "--hidden-import=threading",
            "--hidden-import=socket",
            "--hidden-import=ssl",
            "--hidden-import=json",
            "--hidden-import=hashlib",
            "--hidden-import=hmac",
            "--hidden-import=base64",
            "--hidden-import=zlib",
            "--hidden-import=sqlite3",
            "--hidden-import=requests",
            "--hidden-import=scapy",
            "--hidden-import=nmap",
            "--hidden-import=cryptography",
            "--hidden-import=dnspython",
            "--hidden-import=concurrent.futures",
            "--hidden-import=dataclasses",
            "--hidden-import=typing",
            "--hidden-import=logging",
            "--hidden-import=random",
            "--hidden-import=string",
            "--hidden-import=time",
            "--hidden-import=datetime",
            "--hidden-import=os",
            "--hidden-import=sys",
            "--hidden-import=pathlib",
            "main.py"
        ])
        
        print("Executable built successfully!")
        print("Output: dist/VexityBot.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    
    return True

def create_installer():
    """Create installer script"""
    installer_content = '''
@echo off
echo VexityBot Installer
echo ===================

echo Creating VexityBot directory...
mkdir "C:\\VexityBot" 2>nul

echo Copying files...
copy "dist\\VexityBot.exe" "C:\\VexityBot\\"
copy "main_gui.py" "C:\\VexityBot\\"
copy "VexityBotCore.py" "C:\\VexityBot\\"
copy "VexityBotNetworking.py" "C:\\VexityBot\\"
copy "VexityBotJavaFX.java" "C:\\VexityBot\\"
copy "VexityBotCpp.h" "C:\\VexityBot\\"
copy "VexityBotCpp.cpp" "C:\\VexityBot\\"
copy "VexityBotCSharp.cs" "C:\\VexityBot\\"
copy "requirements.txt" "C:\\VexityBot\\"

echo Creating desktop shortcut...
echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\VexityBot.url"
echo URL=file:///C:/VexityBot/VexityBot.exe >> "%USERPROFILE%\\Desktop\\VexityBot.url"
echo IconFile=C:\\VexityBot\\VexityBot.exe >> "%USERPROFILE%\\Desktop\\VexityBot.url"
echo IconIndex=0 >> "%USERPROFILE%\\Desktop\\VexityBot.url"

echo Installation complete!
echo VexityBot has been installed to C:\\VexityBot
echo Desktop shortcut created.
pause
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content)
    
    print("Installer script created: install.bat")

def create_readme():
    """Create README file"""
    readme_content = '''
# VexityBot - Advanced Bot Management System

## Overview
VexityBot is a comprehensive bot management system with full-stack capabilities across multiple programming languages.

## Features
- 23 specialized bots with unique capabilities
- Advanced attack implementations
- Real-time network communication
- Database integration
- Multi-language support (Python, Java, C++, C#)
- Modern GUI interface
- Coordinated attack capabilities

## Installation
1. Run install.bat as administrator
2. VexityBot will be installed to C:\\VexityBot
3. Desktop shortcut will be created

## Usage
1. Double-click VexityBot.exe to start
2. Use the GUI to manage bots and launch attacks
3. Each bot has its own admin panel with specialized controls

## Bot Specializations
- AlphaBot: Nuclear Warfare
- BetaBot: Cyber Warfare
- GammaBot: Stealth Operations
- DeltaBot: EMP Warfare
- EpsilonBot: Biological Warfare
- ZetaBot: Gravity Control
- EtaBot: Thermal Annihilation
- ThetaBot: Cryogenic Freeze
- IotaBot: Quantum Entanglement
- KappaBot: Dimensional Portal
- LambdaBot: Neural Network
- MuBot: Molecular Disassembly
- NuBot: Sound Wave Devastation
- XiBot: Light Manipulation
- OmicronBot: Dark Matter Control
- PiBot: Mathematical Chaos
- RhoBot: Chemical Reactions
- SigmaBot: Magnetic Fields
- TauBot: Time Manipulation
- UpsilonBot: Space-Time Fabric
- PhiBot: Consciousness Control
- ChiBot: Energy Vortex
- PsiBot: Psychic Warfare

## Requirements
- Windows 10/11
- .NET Framework 4.8
- Java Runtime Environment 11+
- Visual C++ Redistributable

## Support
For support and updates, contact the development team.

## License
Proprietary - All rights reserved.
'''
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("README.md created")

def main():
    """Main build process"""
    print("VexityBot Executable Builder")
    print("============================")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create spec file
    create_spec_file()
    
    # Create icon
    create_icon()
    
    # Build executable
    if build_executable():
        print("\nBuild completed successfully!")
        
        # Create installer
        create_installer()
        
        # Create README
        create_readme()
        
        print("\nFiles created:")
        print("- dist/VexityBot.exe (main executable)")
        print("- install.bat (installer script)")
        print("- README.md (documentation)")
        print("- VexityBot.spec (PyInstaller spec)")
        
        print("\nTo install VexityBot:")
        print("1. Run install.bat as administrator")
        print("2. VexityBot will be installed to C:\\VexityBot")
        
    else:
        print("Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
