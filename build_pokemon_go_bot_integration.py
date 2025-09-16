#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for Pokemon Go Bot Integration with VexityBot GUI
Integrates the Spring Boot Pokemon Go Bot with the VexityBot GUI system
"""

import os
import sys
import subprocess
import shutil
import json
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

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    dependencies = [
        "flask",
        "flask-cors",
        "requests",
        "beautifulsoup4",
        "geopy"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {dep}")

def create_pokemon_go_bot_jar():
    """Create Pokemon Go Bot Spring Boot JAR wrapper"""
    print("Creating Pokemon Go Bot Spring Boot JAR...")
    
    jar_content = '''#!/usr/bin/env python3
"""
Pokemon Go Bot Spring Boot JAR Wrapper
Python implementation of the Kotlin Spring Boot application
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PokemonGoBot_SpringBoot_Application import PokemonGoBotSpringBootApp

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Pokemon Go Bot Spring Boot Application')
    parser.add_argument('--server.port', default=8080, type=int, help='Server port')
    parser.add_argument('--spring.profiles.active', default='dev', help='Spring profile')
    
    args = parser.parse_args()
    
    app = PokemonGoBotSpringBootApp(port=args.server.port, profile=args.spring.profiles.active)
    app.run(debug=args.spring.profiles.active == 'dev')
'''
    
    with open('pokemon-go-bot.py', 'w') as f:
        f.write(jar_content)
    
    # Make it executable
    os.chmod('pokemon-go-bot.py', 0o755)
    print("✓ Pokemon Go Bot JAR wrapper created")

def create_config_files():
    """Create configuration files"""
    print("Creating configuration files...")
    
    # Create config directory
    os.makedirs('config', exist_ok=True)
    
    # Spring Boot configuration
    spring_config = {
        'enabled': True,
        'base_url': 'http://localhost:8080',
        'api_endpoint': '/api/bot',
        'auth_endpoint': '/api/bot/{bot_name}/auth',
        'status_endpoint': '/api/bot/{bot_name}/status',
        'control_endpoint': '/api/bot/{bot_name}/control',
        'data_endpoint': '/api/bot/{bot_name}/data',
        'config_endpoint': '/api/bot/{bot_name}/config',
        'jar_file': 'pokemon-go-bot.py',
        'config_file': 'bot-config.json',
        'java_executable': 'python',
        'spring_profile': 'dev',
        'server_port': 8080,
        'auto_start': True,
        'auto_restart': True,
        'restart_delay': 5
    }
    
    with open('pokemon_go_bot_config.json', 'w') as f:
        json.dump(spring_config, f, indent=2)
    print("✓ Spring Boot configuration created")
    
    # Example bot configuration
    example_bot_config = {
        'bot_name': 'example_bot',
        'enabled': True,
        'location': {
            'lat': 40.7589,
            'lng': -73.9851,
            'alt': 10
        },
        'credentials': {
            'username': 'your_username',
            'password': 'your_password',
            'auth_type': 'PTC'
        },
        'settings': {
            'walk_speed': 4.16,
            'catch_pokemon': True,
            'spin_pokestops': True,
            'battle_gyms': False,
            'catch_legendary': True,
            'catch_shiny': True,
            'transfer_duplicates': True,
            'min_cp_threshold': 100,
            'max_pokemon_storage': 1000
        },
        'advanced': {
            'human_like_delays': True,
            'random_movements': True,
            'smart_timing': True,
            'ban_bypass': True,
            'ai_automation': True
        }
    }
    
    with open('config/example_bot.json', 'w') as f:
        json.dump(example_bot_config, f, indent=2)
    print("✓ Example bot configuration created")

def create_vexitybot_integration():
    """Create VexityBot integration file"""
    print("Creating VexityBot integration...")
    
    integration_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VexityBot Pokemon Go Bot Integration
Adds Pokemon Go Bot management to the main VexityBot GUI
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PokemonGoBot_GUI_Integration import PokemonGoBotGUITab

def add_pokemon_go_bot_tab(notebook, gui_callback=None):
    """Add Pokemon Go Bot tab to VexityBot notebook"""
    try:
        # Create Pokemon Go Bot tab
        pokemon_tab = PokemonGoBotGUITab(notebook, gui_callback)
        
        # Add to notebook
        notebook.add(pokemon_tab.parent, text="Pokemon Go Bot")
        
        print("✅ Pokemon Go Bot tab added to VexityBot GUI")
        return pokemon_tab
        
    except Exception as e:
        print(f"❌ Error adding Pokemon Go Bot tab: {e}")
        return None

# Example usage for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("VexityBot Pokemon Go Bot Integration Test")
    root.geometry("1000x700")
    
    # Create notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    # Add Pokemon Go Bot tab
    pokemon_tab = add_pokemon_go_bot_tab(notebook)
    
    if pokemon_tab:
        print("✅ Pokemon Go Bot integration test successful")
    else:
        print("❌ Pokemon Go Bot integration test failed")
    
    root.mainloop()
'''
    
    with open('VexityBot_PokemonGoBot_Integration.py', 'w') as f:
        f.write(integration_content)
    print("✓ VexityBot integration created")

def build_executable():
    """Build the integrated executable"""
    print("Building integrated executable...")
    
    try:
        # Build command with all Pokemon Go Bot files
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=VexityBot_PokemonGoBot_Ultimate",
            "--add-data=Thunderbolt_PokemonGO_Bot.py;.",
            "--add-data=PokemonGoBot_SpringBoot_Integration.py;.",
            "--add-data=PokemonGoBot_GUI_Integration.py;.",
            "--add-data=PokemonGoBot_SpringBoot_Application.py;.",
            "--add-data=VexityBot_PokemonGoBot_Integration.py;.",
            "--add-data=pokemon-go-bot.py;.",
            "--add-data=pokemon_go_bot_config.json;.",
            "--add-data=config;config",
            "--hidden-import=flask",
            "--hidden-import=flask_cors",
            "--hidden-import=requests",
            "--hidden-import=beautifulsoup4",
            "--hidden-import=geopy",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.scrolledtext",
            "--hidden-import=threading",
            "--hidden-import=time",
            "--hidden-import=datetime",
            "--hidden-import=json",
            "--hidden-import=logging",
            "--exclude-module=matplotlib",
            "--exclude-module=numpy",
            "--exclude-module=pandas",
            "--exclude-module=scipy",
            "--exclude-module=sklearn",
            "--exclude-module=tensorflow",
            "--exclude-module=torch",
            "main_gui.py"
        ]
        
        print("Running PyInstaller...")
        subprocess.check_call(cmd)
        
        print("✓ Integrated executable built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_package():
    """Create complete package"""
    print("Creating complete package...")
    
    package_dir = "VexityBot_PokemonGoBot_Complete"
    
    # Remove existing package
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    # Create package directory
    os.makedirs(package_dir)
    
    # Copy executable
    if os.path.exists("dist/VexityBot_PokemonGoBot_Ultimate.exe"):
        shutil.copy2("dist/VexityBot_PokemonGoBot_Ultimate.exe", package_dir)
        print("✓ Copied executable")
    else:
        print("✗ Executable not found!")
        return False
    
    # Copy Pokemon Go Bot files
    pokemon_files = [
        "Thunderbolt_PokemonGO_Bot.py",
        "PokemonGoBot_SpringBoot_Integration.py",
        "PokemonGoBot_GUI_Integration.py",
        "PokemonGoBot_SpringBoot_Application.py",
        "VexityBot_PokemonGoBot_Integration.py",
        "pokemon-go-bot.py",
        "pokemon_go_bot_config.json",
        "test_pokemon_map_integration.py",
        "POKEMON_MAP_INTEGRATION_README.md"
    ]
    
    for file in pokemon_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✓ Copied {file}")
    
    # Copy config directory
    if os.path.exists("config"):
        shutil.copytree("config", os.path.join(package_dir, "config"))
        print("✓ Copied config directory")
    
    # Create launcher script
    launcher_content = '''@echo off
echo VexityBot Pokemon Go Bot Ultimate
echo =================================
echo Starting VexityBot with Pokemon Go Bot integration...
echo.

REM Start Spring Boot backend
echo Starting Pokemon Go Bot Spring Boot backend...
start "Pokemon Go Bot Backend" python pokemon-go-bot.py

REM Wait for backend to start
timeout /t 5 /nobreak > nul

REM Start VexityBot GUI
echo Starting VexityBot GUI...
VexityBot_PokemonGoBot_Ultimate.exe

echo.
echo VexityBot Pokemon Go Bot Ultimate started!
pause
'''
    
    with open(os.path.join(package_dir, "start_vexitybot_pokemon_go.bat"), 'w') as f:
        f.write(launcher_content)
    print("✓ Created launcher script")
    
    # Create README
    readme_content = """# VexityBot Pokemon Go Bot Ultimate v2.0.0

## 🚀 Quick Start
1. Double-click `start_vexitybot_pokemon_go.bat` to start everything
2. Or run `VexityBot_PokemonGoBot_Ultimate.exe` for GUI only

## ✨ Features
- **Complete VexityBot GUI** with all original features
- **Pokemon Go Bot Integration** with Spring Boot backend
- **Real-time Pokemon Map** integration with pokemap.net
- **Bot Management System** for multiple Pokemon Go bots
- **Advanced Statistics** and monitoring
- **Configuration Management** for all bots
- **Map-based Navigation** and route optimization

## 🤖 Pokemon Go Bot Features

### Map Integration
- Real-time Pokemon tracking from pokemap.net
- Pokestop and Gym discovery
- Nest detection and monitoring
- Weather integration for spawn boosts

### Smart Navigation
- Optimal route calculation
- Rare Pokemon prioritization
- Auto-navigation to targets
- Distance-based filtering

### Bot Management
- Multiple bot instances
- Individual bot configuration
- Real-time status monitoring
- Start/stop controls

### Advanced Analytics
- Map heatmap generation
- Pokemon type filtering
- Rarity analysis
- Export/import functionality

## 🎮 How to Use

### Starting the Application
1. **Run `start_vexitybot_pokemon_go.bat`** - Starts everything (recommended)
2. **Run `VexityBot_PokemonGoBot_Ultimate.exe`** - GUI only (backend must be running)

### Pokemon Go Bot Tab
1. **Bot Management**: Add, configure, and manage Pokemon Go bots
2. **Statistics**: View real-time statistics and performance
3. **Configuration**: Configure Spring Boot backend and bot settings
4. **Logs**: Monitor bot activity and debug information

### Bot Configuration
1. Go to the Pokemon Go Bot tab
2. Click "Add New Bot" to create a new bot
3. Configure credentials and location
4. Start the bot and monitor its progress

## 🔧 Configuration

### Spring Boot Backend
- **Port**: 8080 (default)
- **Profile**: dev (development mode)
- **Auto-start**: Enabled by default
- **Auto-restart**: Enabled for reliability

### Bot Settings
- **Location**: Set latitude/longitude coordinates
- **Credentials**: PTC or Google authentication
- **Settings**: Walk speed, catch preferences, etc.
- **Advanced**: AI automation, ban bypass, etc.

## 📁 File Structure
```
VexityBot_PokemonGoBot_Complete/
├── VexityBot_PokemonGoBot_Ultimate.exe    # Main executable
├── start_vexitybot_pokemon_go.bat         # Launcher script
├── pokemon-go-bot.py                      # Spring Boot backend
├── Thunderbolt_PokemonGO_Bot.py           # Pokemon Go Bot core
├── PokemonGoBot_SpringBoot_Integration.py # Backend integration
├── PokemonGoBot_GUI_Integration.py        # GUI integration
├── PokemonGoBot_SpringBoot_Application.py # Spring Boot app
├── VexityBot_PokemonGoBot_Integration.py  # VexityBot integration
├── pokemon_go_bot_config.json             # Configuration
├── config/                                # Bot configurations
│   └── example_bot.json
└── README.txt                             # This file
```

## 🚨 Important Notes

- **Internet Required**: Pokemon Go Bot needs internet for map data
- **Credentials**: Configure your Pokemon Go Trainer Club credentials
- **Location**: Set your location for accurate Pokemon tracking
- **Legal**: Use responsibly and in accordance with Pokemon GO ToS

## 🎯 Bot Modes

### Catching Mode
- Uses map data to find nearby Pokemon
- Prioritizes rare Pokemon (shiny, legendary, high CP/IV)
- Navigates to closest Pokemon automatically
- Spins nearby Pokestops

### Map Mode
- Focuses on map data analysis
- Shows comprehensive area information
- Calculates optimal routes
- Monitors rare Pokemon spawns

### Exploring Mode
- Follows calculated optimal routes
- Visits high-priority locations
- Balances Pokemon catching and Pokestop spinning

## 📞 Support

For issues or questions:
1. Check the Pokemon Go Bot tab logs
2. Verify Spring Boot backend is running
3. Check your internet connection
4. Ensure credentials are correct

---

**VexityBot Pokemon Go Bot Ultimate v2.0.0**
*Complete Pokemon Go Bot Management System with VexityBot Integration*
"""
    
    with open(os.path.join(package_dir, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ Created README")
    
    print(f"\n✓ Complete package created: {package_dir}/")
    return True

def main():
    """Main build process"""
    print("VexityBot Pokemon Go Bot Integration Build")
    print("==========================================")
    print()
    
    # Step 1: Clean build
    clean_build()
    print()
    
    # Step 2: Install dependencies
    install_dependencies()
    print()
    
    # Step 3: Create Pokemon Go Bot JAR
    create_pokemon_go_bot_jar()
    print()
    
    # Step 4: Create configuration files
    create_config_files()
    print()
    
    # Step 5: Create VexityBot integration
    create_vexitybot_integration()
    print()
    
    # Step 6: Build executable
    if not build_executable():
        print("\n❌ Build failed!")
        return False
    print()
    
    # Step 7: Create package
    if not create_package():
        print("\n❌ Package creation failed!")
        return False
    print()
    
    # Success message
    print("="*70)
    print("🎉 BUILD COMPLETED SUCCESSFULLY! 🎉")
    print("="*70)
    print()
    print("📁 Files created:")
    print("   • dist/VexityBot_PokemonGoBot_Ultimate.exe (executable)")
    print("   • VexityBot_PokemonGoBot_Complete/ (complete package)")
    print()
    print("🚀 To run VexityBot Pokemon Go Bot Ultimate:")
    print("   1. Go to VexityBot_PokemonGoBot_Complete/ folder")
    print("   2. Double-click start_vexitybot_pokemon_go.bat")
    print("   3. Or run VexityBot_PokemonGoBot_Ultimate.exe")
    print()
    print("✨ Features included:")
    print("   • Complete VexityBot GUI with all features")
    print("   • Pokemon Go Bot Spring Boot backend")
    print("   • Real-time Pokemon Map integration")
    print("   • Multiple bot management")
    print("   • Advanced statistics and monitoring")
    print("   • Configuration management")
    print("   • Map-based navigation")
    print()
    print("🎮 Pokemon Go Bot Features:")
    print("   • Real-time Pokemon tracking")
    print("   • Pokestop and Gym discovery")
    print("   • Nest detection")
    print("   • Weather integration")
    print("   • Smart navigation")
    print("   • Route optimization")
    print("   • Rare Pokemon prioritization")
    print("   • Map heatmap generation")
    print()
    print("Enjoy using VexityBot Pokemon Go Bot Ultimate! 🤖⚡")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Build failed! Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Build completed successfully!")
