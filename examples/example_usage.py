#!/usr/bin/env python3
"""
VexityBot Example Usage Script
Demonstrates basic bot management operations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_gui import VexityBotGUI
import tkinter as tk

def main():
    """Example usage of VexityBot"""
    print("VexityBot Example Usage")
    print("======================")
    
    # Create GUI
    root = tk.Tk()
    app = VexityBotGUI(root)
    
    print("Starting VexityBot GUI...")
    print("Use the interface to manage your bots!")
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
