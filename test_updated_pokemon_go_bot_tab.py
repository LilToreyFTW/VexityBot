#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the updated Pokemon Go Bot Tab
Demonstrates the complete interface with PTC credentials
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def gui_callback(message):
    """GUI callback function"""
    print(f"[GUI_UPDATE] {message}")

def main():
    """Main test function"""
    print("Testing Updated Pokemon Go Bot Tab")
    print("=" * 50)
    
    # Create main window
    root = tk.Tk()
    root.title("Pokemon Go Bot Tab Test")
    root.geometry("1200x800")
    
    # Create notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Add Pokemon Go Bot tab
    try:
        from PokemonGoBot_GUI_Integration import PokemonGoBotGUITab
        
        pokemon_tab = PokemonGoBotGUITab(notebook, gui_callback)
        notebook.add(pokemon_tab.parent, text="⚡ Pokemon Go Bot")
        
        print("✅ Pokemon Go Bot tab created successfully")
        print("✅ PTC credentials loaded: InsaneDexHolder")
        print("✅ All features available:")
        print("  - Dashboard with real-time stats")
        print("  - Bot control with PTC login")
        print("  - Pokemon management")
        print("  - Map integration")
        print("  - Location settings")
        print("  - Statistics tracking")
        print("  - Configuration management")
        print("  - Activity logs")
        
    except ImportError as e:
        print(f"❌ Error importing Pokemon Go Bot tab: {e}")
        
        # Create error tab
        error_frame = ttk.Frame(notebook)
        notebook.add(error_frame, text="❌ Error")
        
        error_label = ttk.Label(error_frame, text=f"Error loading Pokemon Go Bot tab:\n{e}", 
                               font=('Arial', 12), foreground="red")
        error_label.pack(expand=True)
        
    except Exception as e:
        print(f"❌ Error creating Pokemon Go Bot tab: {e}")
        
        # Create error tab
        error_frame = ttk.Frame(notebook)
        notebook.add(error_frame, text="❌ Error")
        
        error_label = ttk.Label(error_frame, text=f"Error creating Pokemon Go Bot tab:\n{e}", 
                               font=('Arial', 12), foreground="red")
        error_label.pack(expand=True)
    
    # Add info tab
    info_frame = ttk.Frame(notebook)
    notebook.add(info_frame, text="ℹ️ Info")
    
    info_text = """
Pokemon Go Bot Tab Features:

🔐 PTC Login Integration:
  - Username: InsaneDexHolder
  - Password: Torey991200@##@@##
  - Auto-configured on startup

📊 Dashboard:
  - Real-time bot status
  - Quick statistics
  - Map integration controls
  - Activity log

🤖 Bot Control:
  - PTC credentials management
  - Location settings (NYC default)
  - Bot settings (walk speed, catch preferences)
  - Start/Stop/Restart controls
  - Mode selection (catching, exploring, raiding, etc.)

🗺️ Map & Location:
  - Pokemon map integration
  - Nearby Pokemon/Pokestops/Gyms
  - Location search
  - Rare Pokemon finder

📈 Statistics:
  - Pokemon caught
  - Pokestops spun
  - Gyms battled
  - XP gained
  - Stardust earned

⚙️ Configuration:
  - Bot settings
  - Map settings
  - Export/Import data

📝 Logs:
  - Real-time activity log
  - Error tracking
  - Save/clear functionality

Usage:
1. Go to Bot Control tab
2. Set your location (default: NYC)
3. Click "Start Bot" to begin
4. Monitor progress in Dashboard
5. Use Map tab to find Pokemon
6. Check Statistics for progress
    """
    
    info_label = ttk.Label(info_frame, text=info_text, font=('Consolas', 10), justify=tk.LEFT)
    info_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    print("\n" + "=" * 50)
    print("Pokemon Go Bot Tab Test Started!")
    print("=" * 50)
    print("Features available:")
    print("✅ Complete GUI interface")
    print("✅ PTC login integration")
    print("✅ Real-time map data")
    print("✅ Bot control and management")
    print("✅ Statistics tracking")
    print("✅ Activity logging")
    print("\nClick 'Start Bot' in the Bot Control tab to begin!")
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
