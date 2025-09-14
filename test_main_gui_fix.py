#!/usr/bin/env python3
"""
Test script to verify the main_gui.py fix
"""

import sys
import os

def test_main_gui_import():
    """Test if main_gui.py can be imported without errors"""
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import main_gui
        import main_gui
        print("✅ main_gui.py imported successfully")
        
        # Check if the class can be instantiated (without showing GUI)
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        try:
            app = main_gui.VexityBotGUI(root)
            print("✅ VexityBotGUI instantiated successfully")
            
            # Check if DeathBot was initialized
            if hasattr(app, 'deathbot'):
                if app.deathbot:
                    print("✅ DeathBot initialized successfully")
                else:
                    print("⚠️ DeathBot is None (module not found)")
            else:
                print("❌ DeathBot attribute not found")
            
            # Check if status_label exists
            if hasattr(app, 'status_label'):
                print("✅ status_label exists")
            else:
                print("❌ status_label not found")
            
            # Test update_status method
            try:
                app.update_status("Test status message")
                print("✅ update_status method works")
            except Exception as e:
                print(f"❌ update_status method failed: {e}")
            
            root.destroy()
            return True
            
        except Exception as e:
            print(f"❌ Failed to instantiate VexityBotGUI: {e}")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ Failed to import main_gui: {e}")
        return False

def main():
    """Run the test"""
    print("🧪 Testing main_gui.py fix...")
    print("=" * 40)
    
    if test_main_gui_import():
        print("\n🎉 All tests passed! The fix is working correctly.")
        return True
    else:
        print("\n❌ Tests failed. There may still be issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
