#!/usr/bin/env python3
"""
Test script to verify Pokemon bot tabs are working
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_pokemon_tabs():
    """Test if Pokemon bot tabs are accessible"""
    print("🔍 Testing Pokemon Bot Tabs...")
    print("=" * 50)
    
    try:
        # Import the main GUI
        from main_gui import VexityBotGUI
        print("✅ VexityBotGUI imported successfully")
        
        # Create a test window
        root = tk.Tk()
        root.title("Pokemon Bot Tabs Test")
        root.geometry("800x600")
        
        # Create the GUI
        gui = VexityBotGUI(root)
        print("✅ VexityBotGUI created successfully")
        
        # Test if GameBots tab exists
        gamebots_tab_found = False
        for i in range(gui.notebook.index("end")):
            tab_text = gui.notebook.tab(i, "text")
            if "GameBots" in tab_text:
                gamebots_tab_found = True
                print(f"✅ GameBots tab found: {tab_text}")
                break
        
        if not gamebots_tab_found:
            print("❌ GameBots tab not found!")
            print("Available tabs:")
            for i in range(gui.notebook.index("end")):
                tab_text = gui.notebook.tab(i, "text")
                print(f"  - {tab_text}")
            return False
        
        # Test if Thunderbolt methods exist
        thunderbolt_methods = [
            'create_thunderbolt_pokemongo_panel',
            'create_thunderbolt_advanced_bot_panel', 
            'create_thunderbolt_pokemon_data_panel',
            'load_pokemon_data',
            'search_pokemon',
            'on_pokemon_select'
        ]
        
        print("\n🎮 Testing Thunderbolt Pokemon methods...")
        for method in thunderbolt_methods:
            if hasattr(gui, method):
                print(f"✅ {method} method exists")
            else:
                print(f"❌ {method} method missing")
        
        # Test PokemonDataManager
        try:
            from PokemonDataManager import PokemonDataManager
            data_manager = PokemonDataManager()
            print(f"✅ PokemonDataManager loaded: {len(data_manager.pokemon_data)} Pokemon")
        except Exception as e:
            print(f"❌ PokemonDataManager error: {e}")
        
        print("\n🎉 Pokemon Bot Tabs Test Complete!")
        print("\n📋 To access Pokemon bot tabs:")
        print("1. Run: python main_gui.py")
        print("2. Click '🎮 GameBots' tab")
        print("3. Click '👑 Crown Panels' button")
        print("4. Click '👑 Thunderbolt' tab")
        print("5. You should see 3 tabs:")
        print("   - 🎮 Basic Control")
        print("   - ⚙️ Advanced Bot")
        print("   - 📊 Pokemon Data")
        
        # Show the window briefly
        root.after(2000, root.destroy)  # Close after 2 seconds
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_pokemon_tabs()
