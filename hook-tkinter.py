# PyInstaller hook for Tkinter
# This hook ensures Tkinter data files are properly included

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

# Collect all Tkinter data files
datas = collect_data_files('tkinter')

# Collect all Tkinter submodules
hiddenimports = collect_submodules('tkinter')

# Add specific Tkinter modules that might be missed
hiddenimports += [
    'tkinter.constants',
    'tkinter.dnd',
    'tkinter.colorchooser',
    'tkinter.commondialog',
    'tkinter.simpledialog',
    'tkinter.font',
    'tkinter.dialog',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'tkinter.scrolledtext',
    'tkinter.ttk',
]

# Ensure Tkinter data directory is included
tkinter_data_dir = None
try:
    import tkinter
    tkinter_data_dir = os.path.dirname(tkinter.__file__)
    if tkinter_data_dir and os.path.exists(tkinter_data_dir):
        datas.append((tkinter_data_dir, 'tkinter'))
except ImportError:
    pass

print(f"Tkinter hook: Found {len(datas)} data files, {len(hiddenimports)} hidden imports")
