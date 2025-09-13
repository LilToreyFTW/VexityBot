#!/usr/bin/env python3
"""
VexityBot Launcher Script
Simple launcher for the VexityBot GUI application
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: VexityBot requires Python 3.7 or higher")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_requirements():
    """Install required packages"""
    try:
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def run_application():
    """Run the main VexityBot application"""
    try:
        print("Starting VexityBot...")
        from main_gui import main
        main()
    except ImportError as e:
        print(f"Error importing main_gui: {e}")
        print("Make sure main_gui.py is in the same directory")
        return False
    except Exception as e:
        print(f"Error running application: {e}")
        return False
    return True

def main():
    """Main launcher function"""
    print("=" * 50)
    print("VexityBot - Full-Stack Development Environment")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if requirements.txt exists
    if os.path.exists("requirements.txt"):
        install_choice = input("Do you want to install/update requirements? (y/n): ").lower()
        if install_choice in ['y', 'yes']:
            if not install_requirements():
                print("Warning: Some requirements may not have installed properly")
    
    # Run the application
    print("\nLaunching VexityBot GUI...")
    if not run_application():
        sys.exit(1)

if __name__ == "__main__":
    main()
