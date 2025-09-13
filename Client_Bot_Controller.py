#!/usr/bin/env python3

"""
Client Bot Controller - Connects to VPS and controls OSRS bot
Creates a GUI for remote bot control
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import json
import threading
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('client_bot_controller.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ClientBotController:
    """Client application for controlling VPS bot"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ShadowStrike OSRS Bot Controller")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0a0a0a')
        
        # Connection settings
        self.vps_host = "YOUR_VPS_IP_HERE"  # Change this to your VPS IP
        self.vps_port = 9999
        self.socket = None
        self.connected = False
        
        # Bot status
        self.bot_status = {
            'running': False,
            'phase': 'Unknown',
            'current_activity': 'Unknown',
            'stats': {}
        }
        
        # Create GUI
        self.create_gui()
        
        # Start status updater
        self.start_status_updater()
        
        logger.info("Client Bot Controller initialized")
    
    def create_gui(self):
        """Create the GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🤖 ShadowStrike OSRS Bot Controller", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Connection frame
        self.create_connection_frame(main_frame)
        
        # Bot control frame
        self.create_bot_control_frame(main_frame)
        
        # Status frame
        self.create_status_frame(main_frame)
        
        # Logs frame
        self.create_logs_frame(main_frame)
    
    def create_connection_frame(self, parent):
        """Create connection settings frame"""
        conn_frame = ttk.LabelFrame(parent, text="🔌 VPS Connection", style='TSM.TLabelframe')
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Connection settings
        settings_frame = ttk.Frame(conn_frame)
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(settings_frame, text="VPS IP:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.host_entry = ttk.Entry(settings_frame, width=20)
        self.host_entry.insert(0, self.vps_host)
        self.host_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(settings_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.port_entry = ttk.Entry(settings_frame, width=10)
        self.port_entry.insert(0, str(self.vps_port))
        self.port_entry.grid(row=0, column=3, padx=(0, 10))
        
        # Connection buttons
        self.connect_btn = ttk.Button(settings_frame, text="🔗 Connect", command=self.connect_to_vps)
        self.connect_btn.grid(row=0, column=4, padx=(0, 5))
        
        self.disconnect_btn = ttk.Button(settings_frame, text="❌ Disconnect", command=self.disconnect_from_vps, state=tk.DISABLED)
        self.disconnect_btn.grid(row=0, column=5)
        
        # Connection status
        self.connection_status = ttk.Label(settings_frame, text="❌ Disconnected", foreground='red')
        self.connection_status.grid(row=1, column=0, columnspan=6, pady=(5, 0))
    
    def create_bot_control_frame(self, parent):
        """Create bot control frame"""
        control_frame = ttk.LabelFrame(parent, text="🎮 Bot Control", style='TSM.TLabelframe')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Control buttons
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = ttk.Button(buttons_frame, text="🚀 Start Bot", command=self.start_bot, state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹️ Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.restart_btn = ttk.Button(buttons_frame, text="🔄 Restart Bot", command=self.restart_bot, state=tk.DISABLED)
        self.restart_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_btn = ttk.Button(buttons_frame, text="📊 Refresh Status", command=self.refresh_status, state=tk.DISABLED)
        self.status_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.logs_btn = ttk.Button(buttons_frame, text="📋 Get Logs", command=self.get_logs, state=tk.DISABLED)
        self.logs_btn.pack(side=tk.LEFT)
    
    def create_status_frame(self, parent):
        """Create status display frame"""
        status_frame = ttk.LabelFrame(parent, text="📊 Bot Status", style='TSM.TLabelframe')
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Status info
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, width=80)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial status
        self.update_status_display()
    
    def create_logs_frame(self, parent):
        """Create logs display frame"""
        logs_frame = ttk.LabelFrame(parent, text="📋 Bot Logs", style='TSM.TLabelframe')
        logs_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Logs text
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=8, width=80)
        self.logs_text.pack(fill=tk.X, padx=10, pady=10)
    
    def connect_to_vps(self):
        """Connect to VPS server"""
        try:
            self.vps_host = self.host_entry.get().strip()
            self.vps_port = int(self.port_entry.get().strip())
            
            # Create socket connection
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout
            
            # Connect to VPS
            self.socket.connect((self.vps_host, self.vps_port))
            self.connected = True
            
            # Update UI
            self.connection_status.config(text="✅ Connected", foreground='green')
            self.connect_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)
            self.restart_btn.config(state=tk.NORMAL)
            self.status_btn.config(state=tk.NORMAL)
            self.logs_btn.config(state=tk.NORMAL)
            
            # Get initial status
            self.refresh_status()
            
            logger.info(f"Connected to VPS at {self.vps_host}:{self.vps_port}")
            messagebox.showinfo("Connected", f"Successfully connected to VPS at {self.vps_host}:{self.vps_port}")
        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            messagebox.showerror("Connection Error", f"Failed to connect to VPS: {e}")
            self.connected = False
    
    def disconnect_from_vps(self):
        """Disconnect from VPS server"""
        try:
            if self.socket:
                self.socket.close()
                self.socket = None
            
            self.connected = False
            
            # Update UI
            self.connection_status.config(text="❌ Disconnected", foreground='red')
            self.connect_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.DISABLED)
            self.restart_btn.config(state=tk.DISABLED)
            self.status_btn.config(state=tk.DISABLED)
            self.logs_btn.config(state=tk.DISABLED)
            
            logger.info("Disconnected from VPS")
            messagebox.showinfo("Disconnected", "Disconnected from VPS")
        
        except Exception as e:
            logger.error(f"Disconnection error: {e}")
    
    def send_command(self, command: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send command to VPS server"""
        if not self.connected or not self.socket:
            messagebox.showerror("Error", "Not connected to VPS")
            return None
        
        try:
            # Send command
            command_data = json.dumps(command).encode('utf-8')
            self.socket.send(command_data)
            
            # Receive response
            response_data = self.socket.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            
            return response
        
        except Exception as e:
            logger.error(f"Command error: {e}")
            messagebox.showerror("Command Error", f"Failed to send command: {e}")
            return None
    
    def start_bot(self):
        """Start the bot on VPS"""
        response = self.send_command({'action': 'start_bot'})
        if response and response.get('success'):
            messagebox.showinfo("Bot Started", "Bot started successfully on VPS")
            self.refresh_status()
        else:
            error_msg = response.get('error', 'Unknown error') if response else 'No response'
            messagebox.showerror("Error", f"Failed to start bot: {error_msg}")
    
    def stop_bot(self):
        """Stop the bot on VPS"""
        response = self.send_command({'action': 'stop_bot'})
        if response and response.get('success'):
            messagebox.showinfo("Bot Stopped", "Bot stopped successfully on VPS")
            self.refresh_status()
        else:
            error_msg = response.get('error', 'Unknown error') if response else 'No response'
            messagebox.showerror("Error", f"Failed to stop bot: {error_msg}")
    
    def restart_bot(self):
        """Restart the bot on VPS"""
        response = self.send_command({'action': 'restart_bot'})
        if response and response.get('success'):
            messagebox.showinfo("Bot Restarted", "Bot restarted successfully on VPS")
            self.refresh_status()
        else:
            error_msg = response.get('error', 'Unknown error') if response else 'No response'
            messagebox.showerror("Error", f"Failed to restart bot: {error_msg}")
    
    def refresh_status(self):
        """Refresh bot status from VPS"""
        response = self.send_command({'action': 'get_status'})
        if response and response.get('success'):
            self.bot_status = response.get('bot_status', {})
            self.update_status_display()
        else:
            error_msg = response.get('error', 'Unknown error') if response else 'No response'
            logger.error(f"Failed to get status: {error_msg}")
    
    def get_logs(self):
        """Get bot logs from VPS"""
        response = self.send_command({'action': 'get_logs'})
        if response and response.get('success'):
            logs = response.get('logs', [])
            self.logs_text.delete(1.0, tk.END)
            for log in logs:
                self.logs_text.insert(tk.END, log)
        else:
            error_msg = response.get('error', 'Unknown error') if response else 'No response'
            logger.error(f"Failed to get logs: {error_msg}")
    
    def update_status_display(self):
        """Update the status display"""
        self.status_text.delete(1.0, tk.END)
        
        status_info = f"""
🤖 ShadowStrike OSRS Bot Status
===============================

Connection: {'✅ Connected' if self.connected else '❌ Disconnected'}
VPS: {self.vps_host}:{self.vps_port}

Bot Status:
• Running: {'✅ Yes' if self.bot_status.get('running', False) else '❌ No'}
• Phase: {self.bot_status.get('phase', 'Unknown')}
• Activity: {self.bot_status.get('current_activity', 'Unknown')}
• Location: {self.bot_status.get('current_location', 'Unknown')}
• Last Update: {self.bot_status.get('last_update', 'Unknown')}

Statistics:
"""
        
        stats = self.bot_status.get('stats', {})
        if stats:
            status_info += f"""• Combat Level: {stats.get('combat_level', 'Unknown')}
• Total Level: {stats.get('total_level', 'Unknown')}
• GP: {stats.get('gp', 0):,}
• Deaths: {stats.get('deaths', 0)}
• Bans: {stats.get('bans', 0)}
• Quests Completed: {stats.get('quests_completed', 0)}

Skills:
"""
            skills = stats.get('skills', {})
            if skills:
                for skill, level in skills.items():
                    status_info += f"• {skill}: {level}\n"
        
        self.status_text.insert(tk.END, status_info)
    
    def start_status_updater(self):
        """Start automatic status updates"""
        def update_loop():
            while True:
                try:
                    if self.connected:
                        self.refresh_status()
                    time.sleep(5)  # Update every 5 seconds
                except Exception as e:
                    logger.error(f"Status update error: {e}")
                    time.sleep(10)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def run(self):
        """Run the client application"""
        try:
            logger.info("Starting Client Bot Controller...")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application error: {e}")
        finally:
            if self.connected:
                self.disconnect_from_vps()

def main():
    """Main function"""
    app = ClientBotController()
    app.run()

if __name__ == "__main__":
    main()
