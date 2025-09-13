#!/usr/bin/env python3
"""
Debug script to find the exact string formatting issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_multi_bomb_content():
    """Test just the multi-bomb content creation"""
    print("🧪 Testing Multi-Bomb Content Creation...")
    
    try:
        from main_gui import VexityBotGUI
        import tkinter as tk
        
        # Create a minimal GUI instance
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = VexityBotGUI(root)
        
        # Test with minimal data
        selected_bombs = ["quantum"]
        print(f"Selected bombs: {selected_bombs}")
        
        # This should work without errors
        content = app.create_multi_bomb_executable_content(selected_bombs)
        print(f"✅ Content created successfully! Length: {len(content)}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_multi_bomb_content()
