#!/usr/bin/env python3
"""
Debug script to test Pokemon panel creation and find the exact error
"""

import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_pokemon_panel():
    """Debug Pokemon panel creation step by step"""
    print("🔍 Debugging Pokemon Panel Creation...")
    print("=" * 50)
    
    try:
        # Step 1: Test PokemonDataManager
        print("1. Testing PokemonDataManager...")
        try:
            from PokemonDataManager import PokemonDataManager
            data_manager = PokemonDataManager()
            print(f"✅ PokemonDataManager loaded: {len(data_manager.pokemon_data)} Pokemon")
        except Exception as e:
            print(f"❌ PokemonDataManager error: {e}")
            traceback.print_exc()
            return False
        
        # Step 2: Test ThunderboltPokemonGOBot
        print("\n2. Testing ThunderboltPokemonGOBot...")
        try:
            from Thunderbolt_PokemonGO_Bot import ThunderboltPokemonGOBot
            print("✅ ThunderboltPokemonGOBot imported successfully")
        except Exception as e:
            print(f"❌ ThunderboltPokemonGOBot error: {e}")
            traceback.print_exc()
            return False
        
        # Step 3: Test main_gui import
        print("\n3. Testing main_gui import...")
        try:
            from main_gui import VexityBotGUI
            print("✅ VexityBotGUI imported successfully")
        except Exception as e:
            print(f"❌ VexityBotGUI error: {e}")
            traceback.print_exc()
            return False
        
        # Step 4: Test GUI creation
        print("\n4. Testing GUI creation...")
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide window
            
            gui = VexityBotGUI(root)
            print("✅ VexityBotGUI created successfully")
        except Exception as e:
            print(f"❌ GUI creation error: {e}")
            traceback.print_exc()
            return False
        
        # Step 5: Test GameBot data
        print("\n5. Testing GameBot data...")
        try:
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
                    print("Available bots:")
                    for bot in gui.gamebot_data:
                        print(f"  - {bot['name']}")
                    return False
            else:
                print("❌ gamebot_data not found")
                return False
        except Exception as e:
            print(f"❌ GameBot data error: {e}")
            traceback.print_exc()
            return False
        
        # Step 6: Test panel creation method
        print("\n6. Testing panel creation method...")
        try:
            # Check if method exists
            if hasattr(gui, 'create_thunderbolt_pokemongo_panel'):
                print("✅ create_thunderbolt_pokemongo_panel method exists")
            else:
                print("❌ create_thunderbolt_pokemongo_panel method missing")
                return False
            
            # Test the method
            test_frame = tk.Frame(root)
            gui.create_thunderbolt_pokemongo_panel(test_frame, thunderbolt)
            print("✅ Thunderbolt Pokemon panel created successfully!")
            
        except Exception as e:
            print(f"❌ Panel creation error: {e}")
            traceback.print_exc()
            return False
        
        # Step 7: Test the actual Crown Panel creation
        print("\n7. Testing Crown Panel creation...")
        try:
            # Create a notebook for testing
            notebook = tk.ttk.Notebook(root)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # Test the Crown Panel creation
            gui.create_gamebot_crown_panel(notebook, thunderbolt)
            print("✅ Crown Panel created successfully!")
            
        except Exception as e:
            print(f"❌ Crown Panel creation error: {e}")
            traceback.print_exc()
            return False
        
        root.destroy()
        
        print("\n🎉 All tests passed! The Pokemon panel should work.")
        print("\n📋 If you're still seeing the generic panel, try:")
        print("1. Close the GUI completely")
        print("2. Run: python main_gui.py")
        print("3. Go to GameBots > Crown Panels > Thunderbolt")
        print("4. You should see the Pokemon tabs now!")
        
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_pokemon_panel()
