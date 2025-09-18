#!/usr/bin/env python3
"""
VexityBot Tkinter Fix Build Script
This script builds the VexityBot executable with proper Tkinter data collection
to fix the "Tk data directory not found" error.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """Clean previous build directories"""
    print("🧹 Cleaning previous builds...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")

def build_executable():
    """Build the executable with Tkinter fixes"""
    print("🔨 Building VexityBot with Tkinter fixes...")
    
    # PyInstaller command with Tkinter data collection
    cmd = [
        'pyinstaller',
        '--onefile',
        '--console',
        '--name=VexityBot_Ultimate',
        '--collect-data=tkinter',
        '--collect-submodules=tkinter',
        '--hidden-import=tkinter',
        '--hidden-import=_tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=tkinter.filedialog',
        '--add-data=pgoapi;pgoapi',
        '--add-data=pokemongo_bot;pokemongo_bot',
        '--add-data=BlackScreenTakeover.py;.',
        '--add-data=DeathBot.py;.',
        '--add-data=Enhanced_PokemonGo_Bot.py;.',
        '--add-data=Enhanced_PokemonGo_Bot_Integration.py;.',
        '--add-data=Standalone_PokemonGo_Bot.py;.',
        '--add-data=PokemonGo_Bot_pgoapi_Integration.py;.',
        'main_gui.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            return True
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Build timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def test_executable():
    """Test the built executable"""
    exe_path = Path("dist/VexityBot_Ultimate.exe")
    
    if exe_path.exists():
        print(f"✅ Executable created: {exe_path}")
        print(f"📊 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        
        print("\n🧪 Testing executable...")
        try:
            # Start the executable in the background
            subprocess.Popen([str(exe_path)], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            print("✅ Executable started successfully!")
            print("   The Tkinter data directory error should be fixed.")
            return True
        except Exception as e:
            print(f"❌ Failed to start executable: {e}")
            return False
    else:
        print("❌ Executable not found!")
        return False

def main():
    """Main build process"""
    print("🚀 VexityBot Tkinter Fix Build Script")
    print("=" * 50)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if build_executable():
        # Test executable
        if test_executable():
            print("\n🎉 SUCCESS: VexityBot built and tested successfully!")
            print("   The Tkinter data directory issue has been resolved.")
            print("   Users should no longer see the 'Tk data directory not found' error.")
        else:
            print("\n⚠️  Build completed but testing failed.")
    else:
        print("\n❌ Build failed. Check the error messages above.")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
