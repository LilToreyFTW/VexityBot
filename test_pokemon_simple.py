#!/usr/bin/env python3
"""
Simple test to check Pokemon panel creation
"""

import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_pokemon_simple():
    """Simple test for Pokemon panel"""
    print("🔍 Simple Pokemon Panel Test...")
    
    try:
        # Test PokemonDataManager
        print("1. Testing PokemonDataManager...")
        from PokemonDataManager import PokemonDataManager
        data_manager = PokemonDataManager()
        print(f"✅ PokemonDataManager: {len(data_manager.pokemon_data)} Pokemon")
        
        # Test ThunderboltPokemonGOBot
        print("2. Testing ThunderboltPokemonGOBot...")
        from Thunderbolt_PokemonGO_Bot import ThunderboltPokemonGOBot
        print("✅ ThunderboltPokemonGOBot imported")
        
        # Test main_gui import
        print("3. Testing main_gui import...")
        from main_gui import VexityBotGUI
        print("✅ VexityBotGUI imported")
        
        # Test GUI creation
        print("4. Testing GUI creation...")
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        
        gui = VexityBotGUI(root)
        print("✅ VexityBotGUI created")
        
        # Test Thunderbolt data
        print("5. Testing Thunderbolt data...")
        thunderbolt = None
        for bot in gui.gamebot_data:
            if bot['name'] == 'Thunderbolt':
                thunderbolt = bot
                break
        
        if thunderbolt:
            print(f"✅ Thunderbolt found: {thunderbolt['name']}")
        else:
            print("❌ Thunderbolt not found")
            return False
        
        # Test panel creation
        print("6. Testing panel creation...")
        test_frame = tk.Frame(root)
        
        # This is where the error might be
        gui.create_thunderbolt_pokemongo_panel(test_frame, thunderbolt)
        print("✅ Panel created successfully!")
        
        root.destroy()
        print("🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_pokemon_simple()
