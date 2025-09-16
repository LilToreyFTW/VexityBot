#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Pokemon Go Bot Tab to Existing VexityBot GUI
Simple integration script to add Pokemon Go Bot functionality to your existing VexityBot
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def add_pokemon_go_bot_tab_to_vexitybot(notebook, gui_callback=None):
    """
    Add Pokemon Go Bot tab to existing VexityBot notebook
    
    Args:
        notebook: The ttk.Notebook widget from your VexityBot GUI
        gui_callback: Optional callback function for status updates
    
    Returns:
        PokemonGoBotGUITab instance or None if error
    """
    try:
        # Import the Pokemon Go Bot GUI integration
        from PokemonGoBot_GUI_Integration import PokemonGoBotGUITab
        
        # Create Pokemon Go Bot tab
        pokemon_tab = PokemonGoBotGUITab(notebook, gui_callback)
        
        # Add to notebook
        notebook.add(pokemon_tab.parent, text="Pokemon Go Bot")
        
        print("✅ Pokemon Go Bot tab added to VexityBot GUI")
        return pokemon_tab
        
    except ImportError as e:
        print(f"❌ Error importing Pokemon Go Bot integration: {e}")
        print("Make sure all required files are present:")
        print("  - PokemonGoBot_GUI_Integration.py")
        print("  - PokemonGoBot_SpringBoot_Integration.py")
        print("  - Thunderbolt_PokemonGO_Bot.py")
        return None
    except Exception as e:
        print(f"❌ Error adding Pokemon Go Bot tab: {e}")
        return None

def integrate_with_main_gui():
    """
    Example integration with main_gui.py
    Add this to your main_gui.py file
    """
    integration_code = '''
# ADD THIS TO YOUR main_gui.py FILE

# Import the Pokemon Go Bot integration
try:
    from add_pokemon_go_bot_to_vexitybot import add_pokemon_go_bot_tab_to_vexitybot
    POKEMON_GO_BOT_AVAILABLE = True
except ImportError:
    POKEMON_GO_BOT_AVAILABLE = False
    print("Pokemon Go Bot integration not available")

# In your main GUI class, add this method:
def add_pokemon_go_bot_tab(self):
    """Add Pokemon Go Bot tab to the notebook"""
    if POKEMON_GO_BOT_AVAILABLE:
        try:
            pokemon_tab = add_pokemon_go_bot_tab_to_vexitybot(self.notebook, self.update_status)
            if pokemon_tab:
                self.pokemon_go_bot_tab = pokemon_tab
                print("✅ Pokemon Go Bot tab added successfully")
            else:
                print("❌ Failed to add Pokemon Go Bot tab")
        except Exception as e:
            print(f"❌ Error adding Pokemon Go Bot tab: {e}")
    else:
        print("❌ Pokemon Go Bot integration not available")

# In your __init__ method, add this call:
# self.add_pokemon_go_bot_tab()  # Add this line after creating the notebook
'''
    
    print("Integration code for main_gui.py:")
    print("=" * 50)
    print(integration_code)
    print("=" * 50)

def create_standalone_test():
    """Create a standalone test for the Pokemon Go Bot integration"""
    print("Creating standalone test...")
    
    test_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone test for Pokemon Go Bot integration
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main test function"""
    root = tk.Tk()
    root.title("VexityBot Pokemon Go Bot Integration Test")
    root.geometry("1200x800")
    
    # Create notebook (simulating VexityBot structure)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Add some example tabs
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Main Tab")
    ttk.Label(tab1, text="This is the main VexityBot tab").pack(pady=20)
    
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Settings")
    ttk.Label(tab2, text="This is the settings tab").pack(pady=20)
    
    # Add Pokemon Go Bot tab
    try:
        from add_pokemon_go_bot_to_vexitybot import add_pokemon_go_bot_tab_to_vexitybot
        
        pokemon_tab = add_pokemon_go_bot_tab_to_vexitybot(notebook)
        
        if pokemon_tab:
            print("✅ Pokemon Go Bot tab added successfully")
        else:
            print("❌ Failed to add Pokemon Go Bot tab")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Status bar
    status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    print("Starting test GUI...")
    root.mainloop()

if __name__ == "__main__":
    main()
'''
    
    with open('test_pokemon_go_bot_integration.py', 'w') as f:
        f.write(test_content)
    
    print("✅ Standalone test created: test_pokemon_go_bot_integration.py")
    print("Run: python test_pokemon_go_bot_integration.py")

def main():
    """Main function"""
    print("VexityBot Pokemon Go Bot Integration Helper")
    print("==========================================")
    print()
    
    print("This script helps you integrate Pokemon Go Bot functionality into your existing VexityBot GUI.")
    print()
    
    print("Available options:")
    print("1. Show integration code for main_gui.py")
    print("2. Create standalone test")
    print("3. Check dependencies")
    print("4. Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            integrate_with_main_gui()
            print()
        elif choice == '2':
            create_standalone_test()
            print()
        elif choice == '3':
            check_dependencies()
            print()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

def check_dependencies():
    """Check if all required dependencies are available"""
    print("Checking dependencies...")
    
    required_files = [
        "PokemonGoBot_GUI_Integration.py",
        "PokemonGoBot_SpringBoot_Integration.py", 
        "Thunderbolt_PokemonGO_Bot.py",
        "PokemonGoBot_SpringBoot_Application.py"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files")
        print("Please run the build script first: python build_pokemon_go_bot_integration.py")
    else:
        print("\n✅ All required files are present")
    
    # Check Python packages
    print("\nChecking Python packages...")
    packages = ['flask', 'flask_cors', 'requests', 'beautifulsoup4', 'geopy']
    
    missing_packages = []
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing {len(missing_packages)} Python packages")
        print("Install with: pip install " + " ".join(missing_packages))
    else:
        print("\n✅ All required Python packages are installed")

if __name__ == "__main__":
    main()
