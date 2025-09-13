#!/usr/bin/env python3
"""
VexityBot Build Script with Pokemon Integration
Builds the complete VexityBot executable with all features
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except:
        print("❌ Python not found!")
        return False
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller is installed")
    except ImportError:
        print("🔄 Installing PyInstaller...")
        if not run_command(f"{sys.executable} -m pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    return True

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    
    dirs_to_clean = ["build", "dist"]
    files_to_clean = ["VexityBot.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}/")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ Removed {file_name}")

def build_executable():
    """Build the VexityBot executable"""
    print("🔨 Building VexityBot executable...")
    
    # PyInstaller command with all necessary options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=VexityBot",
        "--add-data=data;data",
        "--add-data=config;config", 
        "--add-data=imagecoded;imagecoded",
        "--hidden-import=PokemonDataManager",
        "--hidden-import=Thunderbolt_PokemonGO_Bot",
        "--hidden-import=VexityBotSteganography",
        "--hidden-import=VexityBotSteganographyGUI",
        "--hidden-import=ShadowStrike_OSRS_Bot",
        "--hidden-import=VPS_Bot_Server",
        "--hidden-import=Client_Bot_Controller",
        "main_gui_only.py"
    ]
    
    return run_command(" ".join(cmd), "Building VexityBot executable")

def verify_build():
    """Verify the build was successful"""
    exe_path = Path("dist/VexityBot.exe")
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ VexityBot.exe created successfully!")
        print(f"📁 Location: {exe_path.absolute()}")
        print(f"📊 Size: {size_mb:.1f} MB")
        
        # Test launch
        print("🚀 Testing executable launch...")
        try:
            subprocess.Popen([str(exe_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ VexityBot launched successfully!")
        except Exception as e:
            print(f"⚠️ Launch test failed: {e}")
        
        return True
    else:
        print("❌ Build failed - VexityBot.exe not found!")
        return False

def main():
    """Main build process"""
    print("🎮 VexityBot Build Script with Pokemon Integration")
    print("=" * 50)
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed!")
        return False
    
    print()
    
    # Clean previous builds
    clean_build()
    print()
    
    # Build executable
    if not build_executable():
        print("❌ Build failed!")
        return False
    
    print()
    
    # Verify build
    if not verify_build():
        print("❌ Build verification failed!")
        return False
    
    print()
    print("🎉 Build completed successfully!")
    print()
    print("Features included:")
    print("- 24 Specialized Bots (AlphaBot to OmegaBot)")
    print("- GameBots with Crown Panels")
    print("- ShadowStrike OSRS Bot")
    print("- Thunderbolt Pokemon GO Bot")
    print("- Pokemon Data Database")
    print("- Image Steganography")
    print("- VPS Bot Controller")
    print("- Live Screen Sharing")
    print("- PowerShell Integration")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
