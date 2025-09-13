#!/usr/bin/env python3
"""
Debug script to test Thunderbolt Pokemon panel creation
"""

import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_thunderbolt_panel():
    """Test Thunderbolt Pokemon panel creation"""
    print("🔍 Testing Thunderbolt Pokemon Panel Creation...")
    print("=" * 50)
    
    try:
        # Test PokemonDataManager import
        print("1. Testing PokemonDataManager import...")
        from PokemonDataManager import PokemonDataManager
        data_manager = PokemonDataManager()
        print(f"✅ PokemonDataManager loaded: {len(data_manager.pokemon_data)} Pokemon")
        
        # Test ThunderboltPokemonGOBot import
        print("\n2. Testing ThunderboltPokemonGOBot import...")
        from Thunderbolt_PokemonGO_Bot import ThunderboltPokemonGOBot
        print("✅ ThunderboltPokemonGOBot imported successfully")
        
        # Test main_gui import
        print("\n3. Testing main_gui import...")
        from main_gui import VexityBotGUI
        print("✅ VexityBotGUI imported successfully")
        
        # Test if Thunderbolt methods exist
        print("\n4. Testing Thunderbolt methods...")
        gui_methods = [
            'create_thunderbolt_pokemongo_panel',
            'create_thunderbolt_advanced_bot_panel',
            'create_thunderbolt_pokemon_data_panel',
            'load_pokemon_data',
            'search_pokemon',
            'on_pokemon_select'
        ]
        
        for method in gui_methods:
            if hasattr(VexityBotGUI, method):
                print(f"✅ {method} method exists")
            else:
                print(f"❌ {method} method missing")
        
        # Test GameBot data
        print("\n5. Testing GameBot data...")
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        gui = VexityBotGUI(root)
        
        # Check if gamebot_data exists
        if hasattr(gui, 'gamebot_data'):
            print(f"✅ gamebot_data exists with {len(gui.gamebot_data)} bots")
            
            # Find Thunderbolt
            thunderbolt = None
            for bot in gui.gamebot_data:
                if bot['name'] == 'Thunderbolt':
                    thunderbolt = bot
                    break
            
            if thunderbolt:
                print(f"✅ Thunderbolt found: {thunderbolt}")
            else:
                print("❌ Thunderbolt not found in gamebot_data")
        else:
            print("❌ gamebot_data not found")
        
        # Test the actual panel creation
        print("\n6. Testing panel creation...")
        try:
            # Create a test frame
            test_frame = tk.Frame(root)
            
            # Test the panel creation method
            gui.create_thunderbolt_pokemongo_panel(test_frame, thunderbolt)
            print("✅ Thunderbolt Pokemon panel created successfully")
            
        except Exception as e:
            print(f"❌ Error creating Thunderbolt panel: {e}")
            traceback.print_exc()
        
        root.destroy()
        
        print("\n🎉 Thunderbolt Panel Test Complete!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_thunderbolt_panel()
