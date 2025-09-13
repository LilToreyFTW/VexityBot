#!/usr/bin/env python3
"""
VexityBot Complete GUI Build Script
Creates a complete GUI executable with all necessary files
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous builds...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Cleaned {dir_name}")
    
    # Clean .pyc files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
    
    print("✓ Build cleanup completed")

def build_executable():
    """Build the GUI executable"""
    print("Building VexityBot GUI executable...")
    print("====================================")
    
    try:
        # Build command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=VexityBot",
            "--add-data=main_gui.py;.",
            "--exclude-module=dnspython",
            "--exclude-module=scapy", 
            "--exclude-module=nmap",
            "--exclude-module=cryptography",
            "--exclude-module=requests",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=tkinter.scrolledtext",
            "--hidden-import=threading",
            "--hidden-import=time",
            "--hidden-import=datetime",
            "--hidden-import=random",
            "--hidden-import=logging",
            "--hidden-import=os",
            "--hidden-import=sys",
            "--hidden-import=pathlib",
            "main_gui_only.py"
        ]
        
        print("Running PyInstaller...")
        subprocess.check_call(cmd)
        
        print("✓ Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_package():
    """Create complete package with all files"""
    print("Creating complete package...")
    
    package_dir = "VexityBot_Complete"
    
    # Remove existing package
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    # Create package directory
    os.makedirs(package_dir)
    
    # Copy executable
    if os.path.exists("dist/VexityBot.exe"):
        shutil.copy2("dist/VexityBot.exe", package_dir)
        print("✓ Copied VexityBot.exe")
    else:
        print("✗ VexityBot.exe not found!")
        return False
    
    # Copy launcher
    if os.path.exists("run_vexitybot_gui.bat"):
        shutil.copy2("run_vexitybot_gui.bat", package_dir)
        print("✓ Copied launcher script")
    
    # Copy source files
    source_files = [
        "main_gui.py",
        "main_gui_only.py",
        "VexityBotCore.py",
        "VexityBotNetworking.py",
        "VexityBotNetworking_Simple.py",
        "VexityBotJavaFX.java",
        "VexityBotCpp.h",
        "VexityBotCpp.cpp",
        "VexityBotCSharp.cs"
    ]
    
    for file in source_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✓ Copied {file}")
    
    # Create README
    readme_content = """# VexityBot - Advanced Bot Management System v2.0.0

## 🚀 Quick Start
1. Double-click `VexityBot.exe` to start
2. Or run `run_vexitybot_gui.bat` for the full experience

## ✨ Features
- **Complete GUI Interface** with modern design
- **23 Specialized Bots** with individual management
- **Bot Management System** with start/stop controls
- **Attack Coordination** with all bots
- **Real-time Status Monitoring**
- **Database Management** tools
- **Code Editor** with syntax highlighting
- **Data Analysis** tools
- **AI Management** interface
- **Bomb Interface** for coordinated attacks

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
1. **Double-click `VexityBot.exe`** - Starts the main GUI
2. **Run `run_vexitybot_gui.bat`** - Starts with animated banner

### GUI Features
- **Welcome Tab**: Overview and quick start
- **Code Editor**: Python code editing with syntax highlighting
- **Database Tab**: Database management and queries
- **Data Analysis**: Data visualization and analysis tools
- **Bots Tab**: Manage all 23 specialized bots
- **AI Management**: AI bot coordination and control
- **Bomb Interface**: Coordinated attack system
- **Settings**: Application configuration

### Bot Management
1. **View all bots** in the Bots tab
2. **Start/Stop individual bots** using the action buttons
3. **Monitor real-time status** and statistics
4. **Launch coordinated attacks** using the Bomb interface

## 🔧 Technical Details

### System Requirements
- Windows 10/11
- No additional dependencies required
- Standalone executable

### File Structure
```
VexityBot_Complete/
├── VexityBot.exe              # Main executable
├── run_vexitybot_gui.bat      # Launcher script
├── main_gui.py                # GUI source code
├── main_gui_only.py           # GUI-only main file
├── VexityBotCore.py           # Core bot system
├── VexityBotNetworking.py     # Network communication
├── VexityBotNetworking_Simple.py # Simplified networking
├── VexityBotJavaFX.java       # Java implementation
├── VexityBotCpp.h             # C++ header
├── VexityBotCpp.cpp           # C++ implementation
└── VexityBotCSharp.cs         # C# implementation
```

## 🚨 Important Notes

- This is a **standalone executable** - no installation required
- All **23 bots are included** with full functionality
- **Complete GUI interface** with all features
- **No external dependencies** required
- **Real-time monitoring** shows live status updates

## 🎮 Controls

- **GUI Navigation**: Use the tabs to access different features
- **Bot Management**: Use the action buttons on each bot
- **Attack System**: Use the Bomb interface for coordinated attacks
- **Settings**: Configure the application in the Settings tab

## 📞 Support

For issues or questions:
1. Check this README file
2. Ensure all files are present
3. Try running as administrator
4. Check Windows compatibility

---

**VexityBot v2.0.0 - Advanced Bot Management System**
*Complete GUI Application with Full Feature Set*
"""
    
    with open(f"{package_dir}/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✓ Created README.txt")
    
    print(f"\n✓ Complete package created: {package_dir}/")
    return True

def main():
    """Main build process"""
    print("VexityBot Complete GUI Build")
    print("============================")
    print()
    
    # Step 1: Clean build
    clean_build()
    print()
    
    # Step 2: Build executable
    if not build_executable():
        print("\n❌ Build failed!")
        return False
    print()
    
    # Step 3: Create package
    if not create_package():
        print("\n❌ Package creation failed!")
        return False
    print()
    
    # Success message
    print("="*60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY! 🎉")
    print("="*60)
    print()
    print("📁 Files created:")
    print("   • dist/VexityBot.exe (executable)")
    print("   • VexityBot_Complete/ (complete package)")
    print()
    print("🚀 To run VexityBot:")
    print("   1. Go to VexityBot_Complete/ folder")
    print("   2. Double-click VexityBot.exe")
    print("   3. Or run run_vexitybot_gui.bat")
    print()
    print("✨ Features included:")
    print("   • Complete GUI interface")
    print("   • 23 specialized bots")
    print("   • Bot management system")
    print("   • Attack coordination")
    print("   • Real-time monitoring")
    print("   • Database tools")
    print("   • Code editor")
    print("   • Data analysis")
    print("   • AI management")
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
