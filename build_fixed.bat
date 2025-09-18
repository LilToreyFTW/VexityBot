@echo off
echo VexityBot Ultimate Fixed Build Script
echo =====================================
echo Building VexityBot with Tkinter fixes
echo.

echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "VexityBot.spec" del "VexityBot.spec"
if exist "*.spec" del "*.spec"

echo.
echo Installing required dependencies...
pip install pyinstaller pillow psutil

echo.
echo Creating PyInstaller spec file...
python -c "
import PyInstaller.utils.hooks as hooks
import os

# Create spec file with proper Tkinter handling
spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('DEPLOYMENT_GUIDE.md', '.'),
        ('bot_deployment_config.json', '.'),
        ('osrs_bot_requirements.txt', '.'),
        ('pgoapi', 'pgoapi'),
        ('pokemongo_bot', 'pokemongo_bot'),
        ('BlackScreenTakeover.py', '.'),
        ('DeathBot.py', '.'),
        ('Enhanced_PokemonGo_Bot.py', '.'),
        ('Enhanced_PokemonGo_Bot_Integration.py', '.'),
    ],
    hiddenimports=[
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
        'socket',
        'json',
        'threading',
        'time',
        'logging',
        'datetime',
        'random',
        'subprocess',
        'os',
        'sys',
        'pathlib',
        'queue',
        'pickle',
        'asyncio',
        'typing',
        'pgoapi',
        'pgoapi.pgoapi',
        'pgoapi.exceptions',
        'pgoapi.utilities',
        'pgoapi.auth',
        'pgoapi.auth_ptc',
        'pgoapi.auth_google',
        'pgoapi.rpc_api',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
        'opencv-python',
        'pyautogui',
        'requests',
        'urllib3',
        'cryptography',
        'dnspython',
        'scapy',
        'nmap',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VexityBot_Ultimate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

'''

with open('VexityBot_Ultimate.spec', 'w') as f:
    f.write(spec_content)

print('Spec file created successfully!')
"

echo.
echo Building VexityBot Ultimate executable with spec file...
python -m PyInstaller VexityBot_Ultimate.spec --clean --noconfirm

echo.
echo Checking if build was successful...
if exist "dist\VexityBot_Ultimate.exe" (
    echo.
    echo ========================================
    echo SUCCESS: VexityBot Ultimate created!
    echo ========================================
    echo Location: dist\VexityBot_Ultimate.exe
    echo.
    echo File size:
    dir "dist\VexityBot_Ultimate.exe" | findstr "VexityBot_Ultimate.exe"
    echo.
    echo Features included:
    echo - Main VexityBot GUI with all tabs
    echo - Enhanced Pokemon Go Bot with pgoapi
    echo - DeathBot with black screen takeover
    echo - VPS Bot Controller for remote control
    echo - GameBots with ShadowStrike OSRS automation
    echo - Steganography tools
    echo - Database management and data analysis
    echo - AI management and bot control
    echo.
    echo Build completed successfully!
    echo.
    echo Next steps:
    echo 1. Test the executable: dist\VexityBot_Ultimate.exe
    echo 2. The Tkinter data directory issue should be resolved
    echo 3. All Pokemon Go bot features should work
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo VexityBot_Ultimate.exe not found.
    echo Check the error messages above.
    echo.
    echo Common issues:
    echo - Missing dependencies
    echo - Python path issues
    echo - File permission problems
    echo - Tkinter data directory not found
    echo.
)

echo.
echo Build process completed!
pause
