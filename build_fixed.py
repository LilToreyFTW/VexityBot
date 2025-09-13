#!/usr/bin/env python3
"""
VexityBot Fixed Executable Builder
Handles Python 3.13 compatibility issues
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def uninstall_enum34():
    """Uninstall enum34 package if present"""
    try:
        print("Checking for enum34 package...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "enum34", "-y"])
        print("enum34 package removed")
    except subprocess.CalledProcessError:
        print("enum34 package not found or already removed")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    dependencies = [
        "requests",
        "scapy",
        "nmap",
        "cryptography", 
        "dnspython",
        "pyinstaller"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"Installed: {dep}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {dep}: {e}")

def build_executable():
    """Build the executable with proper configuration"""
    print("Building VexityBot executable...")
    
    try:
        # Build command with proper data files
        cmd = [
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
            "--exclude-module=enum34",
            "main.py"
        ]
        
        subprocess.check_call(cmd)
        
        print("Executable built successfully!")
        print("Output: dist/VexityBot.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def create_simple_build():
    """Create a simpler build without problematic modules"""
    print("Creating simplified build...")
    
    try:
        # Simple build command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=VexityBot",
            "--add-data=main_gui.py;.",
            "--add-data=VexityBotCore.py;.",
            "--add-data=VexityBotNetworking.py;.",
            "--exclude-module=enum34",
            "--exclude-module=scapy",
            "--exclude-module=nmap",
            "main.py"
        ]
        
        subprocess.check_call(cmd)
        
        print("Simplified executable built successfully!")
        print("Output: dist/VexityBot.exe")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Simplified build failed: {e}")
        return False

def main():
    """Main build process"""
    print("VexityBot Fixed Executable Builder")
    print("==================================")
    
    # Uninstall enum34
    uninstall_enum34()
    
    # Install dependencies
    install_dependencies()
    
    # Try full build first
    if build_executable():
        print("\nFull build completed successfully!")
    else:
        print("\nFull build failed, trying simplified build...")
        if create_simple_build():
            print("\nSimplified build completed successfully!")
        else:
            print("\nAll builds failed!")
            return False
    
    # Create directories
    os.makedirs("dist", exist_ok=True)
    os.makedirs("VexityBot_Package", exist_ok=True)
    
    # Copy files to package
    files_to_copy = [
        "main_gui.py",
        "VexityBotCore.py", 
        "VexityBotNetworking.py",
        "VexityBotJavaFX.java",
        "VexityBotCpp.h",
        "VexityBotCpp.cpp",
        "VexityBotCSharp.cs",
        "requirements.txt",
        "README.md"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, "VexityBot_Package/")
            print(f"Copied: {file}")
    
    # Copy executable
    if os.path.exists("dist/VexityBot.exe"):
        shutil.copy2("dist/VexityBot.exe", "VexityBot_Package/")
        print("Copied: VexityBot.exe")
    
    print("\nBuild completed successfully!")
    print("Files created:")
    print("- dist/VexityBot.exe (executable)")
    print("- VexityBot_Package/ (complete package)")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
