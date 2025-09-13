#!/usr/bin/env python3
"""
VexityBot Main Build Script
Builds main.py without problematic dependencies
"""

import os
import sys
import subprocess
import shutil

def build_main_executable():
    """Build main.py executable without problematic dependencies"""
    print("Building VexityBot from main.py...")
    print("==================================")
    
    try:
        # Build command without problematic dependencies
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=VexityBot",
            "--exclude-module=dnspython",
            "--exclude-module=scapy", 
            "--exclude-module=nmap",
            "--exclude-module=cryptography",
            "--exclude-module=requests",
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
            "--hidden-import=logging",
            "--hidden-import=random",
            "--hidden-import=string",
            "--hidden-import=time",
            "--hidden-import=datetime",
            "--hidden-import=os",
            "--hidden-import=sys",
            "--hidden-import=pathlib",
            "main_gui_only.py"
        ]
        
        print("Running PyInstaller...")
        subprocess.check_call(cmd)
        
        print("✓ Build completed successfully!")
        print("✓ Executable created: dist/VexityBot.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("VexityBot Main Build")
    print("===================")
    print()
    
    # Clean previous builds
    print("Cleaning previous builds...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    print("✓ Cleaned build artifacts")
    print()
    
    # Build executable
    if build_main_executable():
        print("\n🎉 SUCCESS! VexityBot built successfully!")
        print("📁 Location: dist/VexityBot.exe")
        print("🚀 You can now run VexityBot.exe")
    else:
        print("\n❌ FAILED! Build failed!")
        print("Check the errors above for details.")

if __name__ == "__main__":
    main()
