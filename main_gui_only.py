#!/usr/bin/env python3
"""
VexityBot GUI-Only Version
Simple GUI application without complex dependencies
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import GUI only
try:
    from main_gui import VexityBotGUI
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure main_gui.py is in the same directory")
    sys.exit(1)

class VexityBotMain:
    """Main VexityBot Application Controller - GUI Only Version"""
    
    def __init__(self):
        self.gui = None
        self.running = False
        
        # Setup logging
        self.setup_logging()
        
        # Initialize GUI
        self.initialize_gui()
    
    def setup_logging(self):
        """Setup application logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "vexitybot_gui.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("VexityBot GUI-Only Application initialized")
    
    def initialize_gui(self):
        """Initialize GUI only"""
        try:
            # Create root window
            root = tk.Tk()
            
            # Initialize GUI
            self.gui = VexityBotGUI(root)
            self.logger.info("GUI initialized successfully")
            
        except Exception as e:
            self.logger.error(f"GUI initialization error: {e}")
            raise
    
    def start(self):
        """Start the main application"""
        try:
            self.logger.info("Starting VexityBot GUI-Only Application...")
            self.running = True
            
            # Start GUI
            self.gui.root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Application start error: {e}")
            messagebox.showerror("Error", f"Failed to start application: {e}")
    
    def stop(self):
        """Stop the main application"""
        try:
            self.logger.info("Stopping VexityBot GUI-Only Application...")
            self.running = False
            
            if self.gui and self.gui.root:
                self.gui.root.quit()
                self.gui.root.destroy()
            
            self.logger.info("Application stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Application stop error: {e}")

def main():
    """Main entry point"""
    try:
        # Create and start application
        app = VexityBotMain()
        app.start()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
