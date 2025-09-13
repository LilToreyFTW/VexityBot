#!/usr/bin/env python3
"""
Test script to verify Pokemon bot integration
"""

import sys
import os

def test_pokemon_integration():
    """Test if Pokemon bot integration is working"""
    print("🔍 Testing Pokemon Bot Integration...")
    print("=" * 50)
    
    # Test 1: Check if PokemonDataManager exists
    try:
        from PokemonDataManager import PokemonDataManager
        print("✅ PokemonDataManager imported successfully")
        
        # Test data loading
        data_manager = PokemonDataManager()
        print(f"✅ Pokemon data loaded: {len(data_manager.pokemon_data)} Pokemon")
        
        # Test Pokemon lookup
        mewtwo = data_manager.get_pokemon("Mewtwo")
        if mewtwo:
            print(f"✅ Mewtwo found: {mewtwo['Name']} - Attack: {mewtwo['BaseAttack']}")
        else:
            print("❌ Mewtwo not found")
            
    except ImportError as e:
        print(f"❌ Failed to import PokemonDataManager: {e}")
        return False
    except Exception as e:
        print(f"❌ Error with PokemonDataManager: {e}")
        return False
    
    # Test 2: Check if data files exist
    data_files = [
        "data/pokemon.json",
        "data/types.json", 
        "data/fast_moves.json",
        "data/charged_moves.json",
        "data/items.json"
    ]
    
    print("\n📁 Checking data files...")
    for file in data_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
    
    # Test 3: Check if main_gui has Pokemon methods
    try:
        import main_gui
        print("\n🎮 Checking main_gui integration...")
        
        # Check if Pokemon methods exist
        pokemon_methods = [
            'create_thunderbolt_pokemon_data_panel',
            'load_pokemon_data',
            'search_pokemon',
            'on_pokemon_select',
            'update_pokemon_basic_info'
        ]
        
        for method in pokemon_methods:
            if hasattr(main_gui.VexityBotGUI, method):
                print(f"✅ {method} method exists")
            else:
                print(f"❌ {method} method missing")
                
    except Exception as e:
        print(f"❌ Error checking main_gui: {e}")
        return False
    
    print("\n🎉 Pokemon Bot Integration Test Complete!")
    print("\n📋 To access the Pokemon bot:")
    print("1. Run: python main_gui.py")
    print("2. Click '🎮 GameBots' tab")
    print("3. Click '👑 Crown Panels' button")
    print("4. Click '👑 Thunderbolt' tab")
    print("5. You'll see 3 tabs: Basic Control, Advanced Bot, Pokemon Data")
    
    return True

if __name__ == "__main__":
    test_pokemon_integration()
