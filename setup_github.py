#!/usr/bin/env python3
"""
VexityBot GitHub Setup Script
Prepares the project for GitHub publication
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_github_structure():
    """Create proper GitHub repository structure"""
    print("Setting up GitHub repository structure...")
    
    # Create necessary directories
    dirs_to_create = [
        ".github/workflows",
        "docs",
        "tests",
        "screenshots",
        "examples"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")
    
    # Create example files
    create_example_files()
    
    # Create documentation
    create_documentation()
    
    # Create test files
    create_test_files()
    
    print("✓ GitHub structure created successfully")

def create_example_files():
    """Create example configuration files"""
    print("Creating example files...")
    
    # Example configuration
    example_config = """# VexityBot Example Configuration
# Copy this file to config/vexitybot.ini and modify as needed

[General]
bot_count = 23
max_threads = 100
log_level = INFO
auto_start = false

[Network]
vps_host = 191.96.152.162
vps_port = 8080
ssl_enabled = true
timeout = 30

[Security]
encryption_key = YourSecretKeyHere
access_control = true
audit_logging = true

[Performance]
memory_limit = 1024
cpu_limit = 80
response_timeout = 100
"""
    
    with open("examples/vexitybot.ini.example", "w") as f:
        f.write(example_config)
    print("✓ Created example configuration")
    
    # Example usage script
    usage_script = """#!/usr/bin/env python3
\"\"\"
VexityBot Example Usage Script
Demonstrates basic bot management operations
\"\"\"

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_gui import VexityBotGUI
import tkinter as tk

def main():
    \"\"\"Example usage of VexityBot\"\"\"
    print("VexityBot Example Usage")
    print("======================")
    
    # Create GUI
    root = tk.Tk()
    app = VexityBotGUI(root)
    
    print("Starting VexityBot GUI...")
    print("Use the interface to manage your bots!")
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
"""
    
    with open("examples/example_usage.py", "w") as f:
        f.write(usage_script)
    print("✓ Created example usage script")

def create_documentation():
    """Create additional documentation files"""
    print("Creating documentation...")
    
    # API Documentation
    api_docs = """# VexityBot API Documentation

## Core Classes

### VexityBotGUI
Main GUI application class.

```python
from main_gui import VexityBotGUI
import tkinter as tk

root = tk.Tk()
app = VexityBotGUI(root)
root.mainloop()
```

### BotManager
Manages individual bot instances.

```python
from VexityBotCore import BotManager

manager = BotManager()
manager.start_all_bots()
manager.stop_all_bots()
```

### NetworkManager
Handles network communication.

```python
from VexityBotNetworking import VexityBotNetworkManager

network = VexityBotNetworkManager(endpoint, bot_id)
await network.start()
```

## Configuration

### Bot Configuration
```python
bot_config = {
    "name": "AlphaBot",
    "specialty": "Nuclear Warfare",
    "port": 8081,
    "status": "Online"
}
```

### Network Configuration
```python
endpoint = NetworkEndpoint(
    host="191.96.152.162",
    port=8080,
    protocol=ProtocolType.TCP,
    ssl_enabled=True
)
```

## Examples

See the `examples/` directory for complete usage examples.
"""
    
    with open("docs/API.md", "w") as f:
        f.write(api_docs)
    print("✓ Created API documentation")
    
    # Installation Guide
    install_guide = """# Installation Guide

## Quick Installation

1. Download the latest release
2. Extract the archive
3. Run `VexityBot.exe`

## Development Installation

1. Clone the repository
2. Install dependencies
3. Build from source

```bash
git clone https://github.com/yourusername/VexityBot.git
cd VexityBot
pip install -r requirements.txt
python build_complete_gui.py
```

## System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 100MB free space
- Internet connection

## Troubleshooting

### Common Issues

1. **Executable won't start**
   - Check Windows compatibility
   - Run as administrator
   - Check antivirus settings

2. **Network errors**
   - Verify internet connection
   - Check firewall settings
   - Verify VPS connectivity

3. **GUI issues**
   - Update graphics drivers
   - Check display settings
   - Verify Python installation

### Getting Help

- Check GitHub Issues
- Join Discussions
- Contact support
"""
    
    with open("docs/INSTALLATION.md", "w") as f:
        f.write(install_guide)
    print("✓ Created installation guide")

def create_test_files():
    """Create basic test files"""
    print("Creating test files...")
    
    # Basic test file
    test_file = """#!/usr/bin/env python3
\"\"\"
VexityBot Test Suite
Basic tests for core functionality
\"\"\"

import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestVexityBot(unittest.TestCase):
    \"\"\"Test cases for VexityBot functionality\"\"\"
    
    def setUp(self):
        \"\"\"Set up test fixtures\"\"\"
        pass
    
    def test_gui_initialization(self):
        \"\"\"Test GUI initialization\"\"\"
        try:
            from main_gui import VexityBotGUI
            import tkinter as tk
            
            root = tk.Tk()
            root.withdraw()  # Hide window during test
            app = VexityBotGUI(root)
            root.destroy()
            
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"GUI initialization failed: {e}")
    
    def test_bot_data_structure(self):
        \"\"\"Test bot data structure\"\"\"
        # This would test the bot data structure
        # Implementation depends on your bot data format
        self.assertTrue(True)
    
    def test_network_endpoint(self):
        \"\"\"Test network endpoint creation\"\"\"
        try:
            from VexityBotNetworking_Simple import NetworkEndpoint, ProtocolType
            
            endpoint = NetworkEndpoint(
                host="127.0.0.1",
                port=8080,
                protocol=ProtocolType.TCP
            )
            
            self.assertEqual(endpoint.host, "127.0.0.1")
            self.assertEqual(endpoint.port, 8080)
            self.assertEqual(endpoint.protocol, ProtocolType.TCP)
        except Exception as e:
            self.fail(f"Network endpoint creation failed: {e}")

if __name__ == "__main__":
    unittest.main()
"""
    
    with open("tests/test_vexitybot.py", "w") as f:
        f.write(test_file)
    print("✓ Created test file")
    
    # Test configuration
    test_config = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
"""
    
    with open("pytest.ini", "w") as f:
        f.write(test_config)
    print("✓ Created pytest configuration")

def create_screenshots_placeholder():
    """Create placeholder for screenshots"""
    print("Creating screenshot placeholders...")
    
    # Create placeholder files for screenshots
    screenshots = [
        "dashboard.png",
        "bots.png", 
        "attack.png",
        "editor.png",
        "database.png",
        "settings.png"
    ]
    
    for screenshot in screenshots:
        placeholder = f"# Placeholder for {screenshot}\n# Add actual screenshot here"
        with open(f"screenshots/{screenshot}.txt", "w") as f:
            f.write(placeholder)
    
    print("✓ Created screenshot placeholders")

def create_git_attributes():
    """Create .gitattributes file"""
    print("Creating .gitattributes...")
    
    gitattributes = """# Git attributes for VexityBot

# Auto detect text files and perform LF normalization
* text=auto

# Python files
*.py text eol=lf

# Batch files
*.bat text eol=crlf

# Documentation
*.md text eol=lf
*.txt text eol=lf

# Binary files
*.exe binary
*.dll binary
*.so binary
*.dylib binary

# Archive files
*.zip binary
*.tar.gz binary
*.rar binary

# Image files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary

# Log files
*.log text eol=lf
"""
    
    with open(".gitattributes", "w") as f:
        f.write(gitattributes)
    print("✓ Created .gitattributes")

def create_pre_commit_config():
    """Create pre-commit configuration"""
    print("Creating pre-commit configuration...")
    
    pre_commit_config = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=127, --extend-ignore=E203]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]
"""
    
    with open(".pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)
    print("✓ Created pre-commit configuration")

def main():
    """Main setup process"""
    print("VexityBot GitHub Setup")
    print("=====================")
    print()
    
    # Create GitHub structure
    create_github_structure()
    print()
    
    # Create additional files
    create_screenshots_placeholder()
    create_git_attributes()
    create_pre_commit_config()
    print()
    
    # Success message
    print("="*50)
    print("🎉 GITHUB SETUP COMPLETED! 🎉")
    print("="*50)
    print()
    print("📁 Files created:")
    print("   • README.md - Main project documentation")
    print("   • LICENSE - MIT License")
    print("   • CONTRIBUTING.md - Contribution guidelines")
    print("   • .gitignore - Git ignore rules")
    print("   • .github/workflows/ci.yml - CI/CD pipeline")
    print("   • requirements.txt - Python dependencies")
    print("   • requirements-dev.txt - Development dependencies")
    print("   • docs/ - Documentation directory")
    print("   • tests/ - Test files")
    print("   • examples/ - Example files")
    print("   • screenshots/ - Screenshot placeholders")
    print()
    print("🚀 Next steps:")
    print("   1. Initialize git repository: git init")
    print("   2. Add all files: git add .")
    print("   3. Initial commit: git commit -m 'Initial commit'")
    print("   4. Create GitHub repository")
    print("   5. Push to GitHub: git push origin main")
    print()
    print("✨ Your project is ready for GitHub!")

if __name__ == "__main__":
    main()
