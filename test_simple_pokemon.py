#!/usr/bin/env python3
"""
Test the simplified Pokemon panel
"""

import sys
import os
import tkinter as tk

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_pokemon():
    """Test the simplified Pokemon panel"""
    print("🔍 Testing Simplified Pokemon Panel...")
    
    try:
        from main_gui import VexityBotGUI
        print("✅ VexityBotGUI imported")
        
        root = tk.Tk()
        root.title("Pokemon Panel Test")
        root.geometry("800x600")
        
        gui = VexityBotGUI(root)
        print("✅ VexityBotGUI created")
        
        # Find Thunderbolt
        thunderbolt = None
        for bot in gui.gamebot_data:
            if bot['name'] == 'Thunderbolt':
                thunderbolt = bot
                break
        
        if thunderbolt:
            print(f"✅ Thunderbolt found: {thunderbolt['name']}")
            
            # Test panel creation
            test_frame = tk.Frame(root)
            test_frame.pack(fill=tk.BOTH, expand=True)
            
            gui.create_thunderbolt_pokemongo_panel(test_frame, thunderbolt)
            print("✅ Pokemon panel created successfully!")
            
            # Show for 3 seconds
            root.after(3000, root.destroy)
            root.mainloop()
            
            print("🎉 SUCCESS! The Pokemon panel should now work!")
            return True
        else:
            print("❌ Thunderbolt not found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_pokemon()
