#!/usr/bin/env python3
"""
VexityBot Clean Build Script
Removes all problematic packages and builds minimal version
"""

import os
import sys
import subprocess
import shutil

def remove_problematic_packages():
    """Remove all problematic packages"""
    problematic_packages = [
        "enum34",
        "typing", 
        "scapy",
        "nmap",
        "cryptography",
        "dnspython",
        "requests"
    ]
    
    print("Removing problematic packages...")
    for package in problematic_packages:
        try:
            print(f"Removing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package, "-y"])
            print(f"✓ {package} removed")
        except subprocess.CalledProcessError:
            print(f"✗ {package} not found or already removed")

def install_pyinstaller():
    """Install only PyInstaller"""
    try:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install PyInstaller: {e}")
        return False
    return True

def build_clean_executable():
    """Build clean executable with minimal dependencies"""
    print("Building clean VexityBot executable...")
    
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=VexityBot",
            "--exclude-module=enum34",
            "--exclude-module=typing",
            "--exclude-module=scapy",
            "--exclude-module=nmap",
            "--exclude-module=cryptography",
            "--exclude-module=dnspython",
            "--exclude-module=requests",
            "--exclude-module=concurrent.futures",
            "--exclude-module=dataclasses",
            "main_ultra_simple.py"
        ]
        
        print("Running PyInstaller...")
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_final_package():
    """Create final distribution package"""
    print("Creating final package...")
    
    # Create package directory
    package_dir = "VexityBot_Final"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy executable
    if os.path.exists("dist/VexityBot.exe"):
        shutil.copy2("dist/VexityBot.exe", package_dir)
        print("✓ Copied VexityBot.exe")
    else:
        print("✗ VexityBot.exe not found!")
        return False
    
    # Copy source files
    source_files = [
        "main_simple.py",
        "main_gui.py",
        "VexityBotCore.py",
        "VexityBotNetworking.py",
        "VexityBotJavaFX.java",
        "VexityBotCpp.h",
        "VexityBotCpp.cpp",
        "VexityBotCSharp.cs"
    ]
    
    for file in source_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✓ Copied {file}")
    
    # Create launcher
    launcher_content = '''@echo off
title VexityBot - Advanced Bot Management System
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

echo Starting VexityBot...
VexityBot.exe

if errorlevel 1 (
    echo.
    echo Error starting VexityBot!
    echo Please check that all files are present.
    pause
)
'''
    
    with open(f"{package_dir}/launch.bat", "w") as f:
        f.write(launcher_content)
    print("✓ Created launch.bat")
    
    # Create README
    readme_content = '''# VexityBot - Advanced Bot Management System v2.0.0

## 🚀 Quick Start
1. Double-click `VexityBot.exe` to start
2. Or run `launch.bat` for the full experience

## ✨ Features
- **23 Specialized Bots** with unique capabilities
- **Individual Admin Panels** for each bot
- **Coordinated Attack System** with all bots
- **Real-time Status Monitoring**
- **Modern GUI Interface**

## 🤖 Bot Specializations

| Bot Name | Specialty | Port | Capabilities |
|----------|-----------|------|--------------|
| AlphaBot | Nuclear Warfare | 8081 | Quantum Bombs, Plasma Cannons |
| BetaBot | Cyber Warfare | 8082 | Data Bombs, Code Injectors |
| GammaBot | Stealth Operations | 8083 | Ghost Protocols, Shadow Strikes |
| DeltaBot | EMP Warfare | 8084 | EMP Bombs, Tesla Coils |
| EpsilonBot | Biological Warfare | 8085 | Virus Bombs, DNA Injectors |
| ZetaBot | Gravity Control | 8086 | Gravity Bombs, Black Hole Generators |
| EtaBot | Thermal Annihilation | 8087 | Thermal Bombs, Plasma Torches |
| ThetaBot | Cryogenic Freeze | 8088 | Freeze Bombs, Ice Shards |
| IotaBot | Quantum Entanglement | 8089 | Quantum Bombs, Entanglement Disruptors |
| KappaBot | Dimensional Portal | 8090 | Portal Bombs, Dimension Rifts |
| LambdaBot | Neural Network | 8091 | Neural Bombs, Brain Scramblers |
| MuBot | Molecular Disassembly | 8092 | Molecular Bombs, Atom Splitters |
| NuBot | Sound Wave Devastation | 8093 | Sonic Bombs, Sound Cannons |
| XiBot | Light Manipulation | 8094 | Light Bombs, Laser Cannons |
| OmicronBot | Dark Matter Control | 8095 | Dark Bombs, Void Generators |
| PiBot | Mathematical Chaos | 8096 | Math Bombs, Equation Explosives |
| RhoBot | Chemical Reactions | 8097 | Chemical Bombs, Reaction Catalysts |
| SigmaBot | Magnetic Fields | 8098 | Magnetic Bombs, Field Disruptors |
| TauBot | Time Manipulation | 8099 | Time Bombs, Chronological Disruptors |
| UpsilonBot | Space-Time Fabric | 8100 | Fabric Bombs, Space Rippers |
| PhiBot | Consciousness Control | 8101 | Consciousness Bombs, Mind Erasers |
| ChiBot | Energy Vortex | 8102 | Vortex Bombs, Energy Tornadoes |
| PsiBot | Psychic Warfare | 8103 | Psychic Bombs, Mind Blasts |

## 🎯 How to Use

### Starting the Application
1. **Double-click `VexityBot.exe`** - Starts the main interface
2. **Run `launch.bat`** - Starts with animated banner

### Managing Bots
1. **Start All Bots** - Click "🚀 Start All Bots" button
2. **Stop All Bots** - Click "⏹️ Stop All Bots" button
3. **Individual Control** - Use ▶️/⏹️ buttons on each bot

### Admin Panels
1. **Click the Crown (👑)** button on any bot
2. **Access specialized controls** for that bot
3. **Launch bot-specific attacks**
4. **Overcharge and reset** bot systems

### Coordinated Attacks
1. **Click "💣 Launch Attack"** for coordinated attack
2. **All 23 bots participate** in the attack
3. **Monitor progress** in real-time
4. **Click "⏹️ Stop Attack"** to halt

## 🔧 Technical Details

### System Requirements
- Windows 10/11
- No additional dependencies required
- Standalone executable

### File Structure
```
VexityBot_Final/
├── VexityBot.exe          # Main executable
├── launch.bat             # Launcher script
├── README.txt             # This file
├── main_simple.py         # Python source
├── main_gui.py            # GUI source
├── VexityBotCore.py       # Core bot system
├── VexityBotNetworking.py # Network communication
├── VexityBotJavaFX.java   # Java implementation
├── VexityBotCpp.h         # C++ header
├── VexityBotCpp.cpp       # C++ implementation
└── VexityBotCSharp.cs     # C# implementation
```

## 🚨 Important Notes

- This is a **standalone executable** - no installation required
- All **23 bots are included** with full functionality
- **Admin panels** provide individual bot control
- **Coordinated attacks** use all bots simultaneously
- **Real-time monitoring** shows live status updates

## 🎮 Controls

- **👑 Crown Button** - Open bot admin panel
- **▶️ Play Button** - Start individual bot
- **⏹️ Stop Button** - Stop individual bot
- **🚀 Start All** - Start all 23 bots
- **⏹️ Stop All** - Stop all 23 bots
- **💣 Launch Attack** - Coordinated attack
- **⏹️ Stop Attack** - Stop coordinated attack

## 📞 Support

For issues or questions:
1. Check this README file
2. Ensure all files are present
3. Try running as administrator
4. Check Windows compatibility

---

**VexityBot v2.0.0 - Advanced Bot Management System**
*Built with Python, Java, C++, and C#*
'''
    
    with open(f"{package_dir}/README.txt", "w") as f:
        f.write(readme_content)
    print("✓ Created README.txt")
    
    # Create desktop shortcut
    shortcut_content = '''[InternetShortcut]
URL=file:///C:/VexityBot_Final/VexityBot.exe
IconFile=C:/VexityBot_Final/VexityBot.exe
IconIndex=0
'''
    
    with open(f"{package_dir}/VexityBot.url", "w") as f:
        f.write(shortcut_content)
    print("✓ Created desktop shortcut")
    
    print(f"\n✓ Final package created: {package_dir}/")
    return True

def main():
    """Main build process"""
    print("VexityBot Clean Build Script")
    print("============================")
    print()
    
    # Step 1: Remove problematic packages
    print("Step 1: Removing problematic packages...")
    remove_problematic_packages()
    print()
    
    # Step 2: Install PyInstaller
    print("Step 2: Installing PyInstaller...")
    if not install_pyinstaller():
        print("✗ Failed to install PyInstaller!")
        return False
    print()
    
    # Step 3: Build executable
    print("Step 3: Building executable...")
    if not build_clean_executable():
        print("✗ Build failed!")
        return False
    print()
    
    # Step 4: Create package
    print("Step 4: Creating final package...")
    if not create_final_package():
        print("✗ Package creation failed!")
        return False
    print()
    
    # Success message
    print("="*60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY! 🎉")
    print("="*60)
    print()
    print("📁 Files created:")
    print("   • dist/VexityBot.exe (executable)")
    print("   • VexityBot_Final/ (complete package)")
    print()
    print("🚀 To run VexityBot:")
    print("   1. Go to VexityBot_Final/ folder")
    print("   2. Double-click VexityBot.exe")
    print("   3. Or run launch.bat for full experience")
    print()
    print("✨ Features included:")
    print("   • 23 specialized bots")
    print("   • Individual admin panels")
    print("   • Coordinated attack system")
    print("   • Real-time monitoring")
    print("   • Modern GUI interface")
    print()
    print("Enjoy using VexityBot! 🤖")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Build failed! Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Build completed successfully!")
