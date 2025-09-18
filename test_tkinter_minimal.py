#!/usr/bin/env python3
"""
Minimal test script to verify Tkinter works in PyInstaller
This script tests if the Tkinter data directory issue is resolved
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

def test_tkinter():
    """Test basic Tkinter functionality"""
    try:
        # Create main window
        root = tk.Tk()
        root.title("Tkinter Test - VexityBot")
        root.geometry("400x300")
        
        # Add a label
        label = ttk.Label(root, text="✅ Tkinter is working correctly!")
        label.pack(pady=20)
        
        # Add a button
        def show_message():
            messagebox.showinfo("Success", "Tkinter data directory issue is FIXED!")
        
        button = ttk.Button(root, text="Test Message Box", command=show_message)
        button.pack(pady=10)
        
        # Add status label
        status_label = ttk.Label(root, text="If you can see this window, the Tkinter issue is resolved!")
        status_label.pack(pady=20)
        
        # Add exit button
        exit_button = ttk.Button(root, text="Exit", command=root.quit)
        exit_button.pack(pady=10)
        
        print("✅ Tkinter test window created successfully!")
        print("   If you can see the window, the Tkinter data directory issue is FIXED!")
        
        # Start the GUI
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Tkinter test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing Tkinter in PyInstaller environment...")
    print("=" * 50)
    
    # Test Tkinter
    if test_tkinter():
        print("\n🎉 SUCCESS: Tkinter is working correctly!")
        print("   The Tkinter data directory issue has been resolved.")
    else:
        print("\n❌ FAILED: Tkinter test failed.")
        print("   The Tkinter data directory issue still exists.")
    
    print("\nPress Enter to exit...")
    input()
