# PyInstaller hook for Tkinter
# This hook ensures all Tkinter data files are properly collected

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
import sys

# Collect all Tkinter data files
datas = collect_data_files('tkinter')

# Collect all Tkinter submodules
hiddenimports = collect_submodules('tkinter')

# Add specific Tkinter modules that might be missed
hiddenimports += [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'tkinter.filedialog',
    'tkinter.constants',
    'tkinter.dnd',
    'tkinter.colorchooser',
    'tkinter.commondialog',
    'tkinter.simpledialog',
    'tkinter.font',
    'tkinter.dialog',
    '_tkinter',
]

# Try to find and include Tkinter data directory
try:
    import tkinter
    tkinter_path = os.path.dirname(tkinter.__file__)
    
    # Look for _tk_data directory
    tk_data_path = os.path.join(tkinter_path, '_tk_data')
    if os.path.exists(tk_data_path):
        datas.append((tk_data_path, '_tk_data'))
        print(f"Found Tkinter data directory: {tk_data_path}")
    
    # Look for other potential data directories
    for item in os.listdir(tkinter_path):
        item_path = os.path.join(tkinter_path, item)
        if os.path.isdir(item_path) and ('tk' in item.lower() or 'data' in item.lower()):
            datas.append((item_path, item))
            print(f"Found additional Tkinter directory: {item_path}")
            
except Exception as e:
    print(f"Warning: Could not locate Tkinter data directory: {e}")

print(f"Tkinter hook: Collected {len(datas)} data files and {len(hiddenimports)} hidden imports")
