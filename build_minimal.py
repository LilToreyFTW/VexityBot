#!/usr/bin/env python3
"""
VexityBot Minimal Build Script
Creates executable with minimal dependencies
"""

import os
import sys
import subprocess
import shutil

def uninstall_problematic_packages():
    """Remove problematic packages"""
    problematic = ["enum34", "scapy", "nmap"]
    
    for package in problematic:
        try:
            print(f"Removing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package, "-y"])
        except subprocess.CalledProcessError:
            print(f"{package} not found or already removed")

def install_basic_dependencies():
    """Install only basic dependencies"""
    basic_deps = ["pyinstaller"]
    
    for dep in basic_deps:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {dep}: {e}")

def build_minimal_executable():
    """Build minimal executable"""
    print("Building minimal VexityBot executable...")
    
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=VexityBot",
            "--exclude-module=enum34",
            "--exclude-module=scapy", 
            "--exclude-module=nmap",
            "--exclude-module=cryptography",
            "--exclude-module=dnspython",
            "--exclude-module=requests",
            "main_simple.py"
        ]
        
        subprocess.check_call(cmd)
        print("Minimal executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def create_package():
    """Create distribution package"""
    print("Creating package...")
    
    # Create package directory
    package_dir = "VexityBot_Minimal"
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy executable
    if os.path.exists("dist/VexityBot.exe"):
        shutil.copy2("dist/VexityBot.exe", package_dir)
        print("Copied VexityBot.exe")
    
    # Copy source files
    source_files = [
        "main_simple.py",
        "main_gui.py",
        "VexityBotCore.py",
        "VexityBotNetworking.py",
        "VexityBotJavaFX.java",
        "VexityBotCpp.h",
        "VexityBotCpp.cpp",
        "VexityBotCSharp.cs",
        "README.md"
    ]
    
    for file in source_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"Copied {file}")
    
    # Create launcher
    launcher_content = '''@echo off
title VexityBot
echo Starting VexityBot...
VexityBot.exe
pause
'''
    
    with open(f"{package_dir}/launch.bat", "w") as f:
        f.write(launcher_content)
    
    print("Created launcher.bat")
    
    # Create README
    readme_content = '''# VexityBot Minimal Version

## Quick Start
1. Double-click VexityBot.exe
2. Or run launch.bat

## Features
- 23 specialized bots
- Individual admin panels
- Coordinated attack system
- Real-time status monitoring

## Bot List
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

## Usage
1. Start all bots using the "Start All Bots" button
2. Click the crown (👑) button on any bot to open its admin panel
3. Use "Launch Attack" for coordinated attacks
4. Monitor status in real-time

Enjoy using VexityBot!
'''
    
    with open(f"{package_dir}/README.txt", "w") as f:
        f.write(readme_content)
    
    print("Created README.txt")
    print(f"Package created: {package_dir}/")

def main():
    """Main build process"""
    print("VexityBot Minimal Build Script")
    print("=============================")
    
    # Remove problematic packages
    uninstall_problematic_packages()
    
    # Install basic dependencies
    install_basic_dependencies()
    
    # Build executable
    if build_minimal_executable():
        print("\nBuild successful!")
        
        # Create package
        create_package()
        
        print("\n" + "="*50)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("="*50)
        print("\nFiles created:")
        print("- dist/VexityBot.exe (executable)")
        print("- VexityBot_Minimal/ (complete package)")
        print("\nTo run VexityBot:")
        print("1. Go to VexityBot_Minimal/ folder")
        print("2. Double-click VexityBot.exe")
        print("3. Or run launch.bat")
        
    else:
        print("\nBuild failed!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
