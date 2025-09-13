#!/usr/bin/env python3
"""
Test script to verify Thunderbolt Pokemon panel fix
"""

import sys
import os
import tkinter as tk

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_thunderbolt_fix():
    """Test if Thunderbolt Pokemon panel now works"""
    print("🔍 Testing Thunderbolt Pokemon Panel Fix...")
    print("=" * 50)
    
    try:
        # Import the main GUI
        from main_gui import VexityBotGUI
        print("✅ VexityBotGUI imported successfully")
        
        # Create a test window
        root = tk.Tk()
        root.title("Thunderbolt Fix Test")
        root.geometry("1000x700")
        
        # Create the GUI
        gui = VexityBotGUI(root)
        print("✅ VexityBotGUI created successfully")
        
        # Test PokemonDataManager
        try:
            from PokemonDataManager import PokemonDataManager
            data_manager = PokemonDataManager()
            print(f"✅ PokemonDataManager loaded: {len(data_manager.pokemon_data)} Pokemon")
        except Exception as e:
            print(f"❌ PokemonDataManager error: {e}")
        
        # Test Thunderbolt panel creation
        print("\n🎮 Testing Thunderbolt panel creation...")
        
        # Find Thunderbolt in gamebot_data
        thunderbolt = None
        for bot in gui.gamebot_data:
            if bot['name'] == 'Thunderbolt':
                thunderbolt = bot
                break
        
        if thunderbolt:
            print(f"✅ Thunderbolt found: {thunderbolt['name']}")
            
            # Create a test frame
            test_frame = tk.Frame(root)
            test_frame.pack(fill=tk.BOTH, expand=True)
            
            # Test the panel creation
            try:
                gui.create_thunderbolt_pokemongo_panel(test_frame, thunderbolt)
                print("✅ Thunderbolt Pokemon panel created successfully!")
                print("🎉 The fix worked! You should now see the Pokemon tabs.")
            except Exception as e:
                print(f"❌ Error creating Thunderbolt panel: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Thunderbolt not found in gamebot_data")
        
        # Show the window for a few seconds
        root.after(3000, root.destroy)  # Close after 3 seconds
        root.mainloop()
        
        print("\n🎉 Thunderbolt Fix Test Complete!")
        print("\n📋 To see the Pokemon tabs:")
        print("1. Run: python main_gui.py")
        print("2. Click '🎮 GameBots' tab")
        print("3. Click '👑 Crown Panels' button")
        print("4. Click '👑 Thunderbolt' tab")
        print("5. You should now see 3 tabs:")
        print("   - 🎮 Basic Control")
        print("   - ⚙️ Advanced Bot")
        print("   - 📊 Pokemon Data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_thunderbolt_fix()
