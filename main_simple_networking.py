#!/usr/bin/env python3
"""
VexityBot Main Entry Point - Simplified Version
Complete Bot Management System with Basic Network Integration
"""

import sys
import os
import asyncio
import threading
import tkinter as tk
from tkinter import messagebox
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all components
try:
    from main_gui import VexityBotGUI
    from VexityBotCore import BotManager, BotConfig, AttackType, AttackTarget
    from VexityBotNetworking_Simple import VexityBotNetworkManager, NetworkEndpoint, ProtocolType
    import VexityBotJavaFX
    import VexityBotCpp
    import VexityBotCSharp
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required files are in the same directory")
    sys.exit(1)

class VexityBotMain:
    """Main VexityBot Application Controller - Simplified Version"""
    
    def __init__(self):
        self.gui = None
        self.bot_manager = None
        self.network_manager = None
        self.running = False
        
        # Setup logging
        self.setup_logging()
        
        # Initialize components
        self.initialize_components()
    
    def setup_logging(self):
        """Setup application logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "vexitybot_main.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("VexityBot Main Application initialized (Simplified Version)")
    
    def initialize_components(self):
        """Initialize all application components"""
        try:
            # Initialize bot manager
            self.bot_manager = BotManager()
            self.logger.info("Bot Manager initialized")
            
            # Initialize simplified network manager
            vps_endpoint = NetworkEndpoint(
                host="191.96.152.162",
                port=8080,
                protocol=ProtocolType.TCP,
                ssl_enabled=False,  # Simplified - no SSL
                encryption_key="VexityBot2024SecretKey"
            )
            self.network_manager = VexityBotNetworkManager(vps_endpoint, "MainController")
            self.logger.info("Simplified Network Manager initialized")
            
            # Initialize GUI
            self.gui = VexityBotGUI(tk.Tk())
            self.logger.info("GUI initialized")
            
        except Exception as e:
            self.logger.error(f"Component initialization error: {e}")
            # Continue without network manager if it fails
            self.network_manager = None
            self.logger.warning("Continuing without network manager")
    
    def start(self):
        """Start the main application"""
        try:
            self.logger.info("Starting VexityBot Main Application (Simplified)...")
            self.running = True
            
            # Start network manager if available
            if self.network_manager:
                asyncio.create_task(self.network_manager.start())
            
            # Start GUI
            self.gui.root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Application start error: {e}")
            messagebox.showerror("Error", f"Failed to start application: {e}")
    
    def stop(self):
        """Stop the main application"""
        try:
            self.logger.info("Stopping VexityBot Main Application...")
            self.running = False
            
            # Stop network manager if available
            if self.network_manager:
                asyncio.create_task(self.network_manager.stop())
            
            # Stop bot manager
            if self.bot_manager:
                asyncio.run(self.bot_manager.stop_all_bots())
            
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
