#!/usr/bin/env python3
"""
Test script to verify Tkinter works properly in PyInstaller environment
"""

import sys
import os

def test_tkinter():
    """Test Tkinter functionality"""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        print("✅ Tkinter imported successfully")
        
        # Test basic Tkinter functionality
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test messagebox
        print("✅ Tkinter root window created")
        
        # Test ttk
        style = ttk.Style()
        print("✅ ttk imported and working")
        
        root.destroy()
        print("✅ Tkinter test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Tkinter test failed: {e}")
        return False

def test_pgoapi():
    """Test pgoapi functionality"""
    try:
        # Add pgoapi to path
        pgoapi_path = os.path.join(os.getcwd(), 'pgoapi')
        if pgoapi_path not in sys.path:
            sys.path.insert(0, pgoapi_path)
        
        from pgoapi import PGoApi
        print("✅ pgoapi imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ pgoapi test failed: {e}")
        return False

def main():
    """Main test function"""
    print("VexityBot Tkinter Fix Test")
    print("=" * 30)
    
    # Test Tkinter
    tkinter_ok = test_tkinter()
    
    # Test pgoapi
    pgoapi_ok = test_pgoapi()
    
    print("\n" + "=" * 30)
    if tkinter_ok and pgoapi_ok:
        print("✅ All tests passed! Ready for PyInstaller build.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return tkinter_ok and pgoapi_ok

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
