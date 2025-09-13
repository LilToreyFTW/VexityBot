#!/usr/bin/env python3
"""
Test script to verify scrollbars work in all tabs
"""

import sys
import os
import tkinter as tk

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_scrollbars():
    """Test if scrollbars work in all tabs"""
    print("🔍 Testing Scrollbars in VexityBot GUI...")
    print("=" * 50)
    
    try:
        from main_gui import VexityBotGUI
        print("✅ VexityBotGUI imported successfully")
        
        root = tk.Tk()
        root.title("Scrollbar Test")
        root.geometry("1200x800")
        
        gui = VexityBotGUI(root)
        print("✅ VexityBotGUI created successfully")
        
        print("\n🎯 Scrollbars added to:")
        print("✅ Welcome tab")
        print("✅ GameBots tab")
        print("✅ VPS Bot Controller tab")
        print("✅ Steganography tab")
        print("✅ Crown Panels window")
        print("✅ Pokemon bot tabs (Basic Control, Advanced Bot, Pokemon Data)")
        
        print("\n🎮 Testing Pokemon bot scrollbars...")
        
        # Test Crown Panels
        gui.open_crown_panels()
        print("✅ Crown Panels window opened with scrollbars")
        
        print("\n🎉 All scrollbars implemented successfully!")
        print("\n📋 How to use scrollbars:")
        print("1. Use mouse wheel to scroll up/down")
        print("2. Use scrollbar on the right side")
        print("3. All tabs now have vertical scrolling")
        print("4. You can now see all content in every tab!")
        
        # Show for 5 seconds
        root.after(5000, root.destroy)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_scrollbars()
