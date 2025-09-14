#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TSMPoke Thunderbolt Bridge
Integration layer between TSMPoke desktop app and Thunderbolt Pokemon GO Bot
"""

import json
import sys
import os
import time
import threading
import queue
from datetime import datetime

# Add the parent directory to the path to import Thunderbolt bot
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

try:
    from Thunderbolt_PokemonGO_Bot import ThunderboltPokemonGOBot
except ImportError:
    print("Warning: Thunderbolt bot not found. Some features may not be available.")
    ThunderboltPokemonGOBot = None

class ThunderboltBridge:
    """Bridge between TSMPoke desktop app and Thunderbolt bot"""
    
    def __init__(self):
        self.bot = None
        self.running = False
        self.status_queue = queue.Queue()
        self.stats_queue = queue.Queue()
        self.command_queue = queue.Queue()
        
        # Bot status
        self.status = {
            'running': False,
            'paused': False,
            'mode': 'idle',
            'current_activity': 'Ready',
            'uptime': '0:00:00'
        }
        
        # Bot statistics
        self.stats = {
            'pokemon_caught': 0,
            'pokestops_spun': 0,
            'gyms_battled': 0,
            'raids_completed': 0,
            'xp_gained': 0,
            'stardust_earned': 0,
            'shiny_caught': 0,
            'perfect_iv_caught': 0,
            'start_time': None,
            'current_activity': 'Ready'
        }
        
        # Start command processing thread
        self.command_thread = threading.Thread(target=self._process_commands, daemon=True)
        self.command_thread.start()
    
    def _process_commands(self):
        """Process commands from the desktop app"""
        while True:
            try:
                command = self.command_queue.get(timeout=1)
                self._handle_command(command)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing command: {e}")
    
    def _handle_command(self, command):
        """Handle a command from the desktop app"""
        cmd_type = command.get('type')
        
        if cmd_type == 'start_bot':
            self._start_bot(command.get('mode', 'catching'))
        elif cmd_type == 'stop_bot':
            self._stop_bot()
        elif cmd_type == 'pause_bot':
            self._pause_bot()
        elif cmd_type == 'change_mode':
            self._change_mode(command.get('mode'))
        elif cmd_type == 'get_status':
            self._send_status()
        elif cmd_type == 'get_stats':
            self._send_stats()
        elif cmd_type == 'update_config':
            self._update_config(command.get('config'))
        elif cmd_type == 'export_stats':
            self._export_stats(command.get('filename'))
        elif cmd_type == 'reset_stats':
            self._reset_stats()
    
    def _start_bot(self, mode='catching'):
        """Start the Thunderbolt bot"""
        try:
            if self.bot is None and ThunderboltPokemonGOBot:
                self.bot = ThunderboltPokemonGOBot()
                self.bot.set_gui_callback(self._on_bot_status_update)
            
            if self.bot:
                success = self.bot.start_bot(mode)
                if success:
                    self.status['running'] = True
                    self.status['mode'] = mode
                    self.status['start_time'] = datetime.now()
                    self.running = True
                    self._send_status()
                    print(f"TSMPoke Thunderbolt bot started in {mode} mode")
                else:
                    print("Failed to start Thunderbolt bot")
        except Exception as e:
            print(f"Error starting bot: {e}")
    
    def _stop_bot(self):
        """Stop the Thunderbolt bot"""
        try:
            if self.bot:
                self.bot.stop_bot()
                self.status['running'] = False
                self.status['paused'] = False
                self.running = False
                self._send_status()
                print("TSMPoke Thunderbolt bot stopped")
        except Exception as e:
            print(f"Error stopping bot: {e}")
    
    def _pause_bot(self):
        """Pause/Resume the Thunderbolt bot"""
        try:
            if self.bot:
                self.bot.pause_bot()
                self.status['paused'] = not self.status['paused']
                self._send_status()
                print(f"TSMPoke Thunderbolt bot {'paused' if self.status['paused'] else 'resumed'}")
        except Exception as e:
            print(f"Error pausing bot: {e}")
    
    def _change_mode(self, mode):
        """Change bot mode"""
        try:
            if self.bot:
                self.bot.set_mode(mode)
                self.status['mode'] = mode
                self._send_status()
                print(f"Bot mode changed to: {mode}")
        except Exception as e:
            print(f"Error changing mode: {e}")
    
    def _update_config(self, config):
        """Update bot configuration"""
        try:
            if self.bot:
                self.bot.update_config(config)
                print("Bot configuration updated")
        except Exception as e:
            print(f"Error updating config: {e}")
    
    def _export_stats(self, filename=None):
        """Export bot statistics"""
        try:
            if self.bot:
                success = self.bot.export_stats(filename)
                if success:
                    print(f"Statistics exported to {filename}")
                else:
                    print("Failed to export statistics")
        except Exception as e:
            print(f"Error exporting stats: {e}")
    
    def _reset_stats(self):
        """Reset bot statistics"""
        try:
            if self.bot:
                self.bot.reset_stats()
                self.stats = self.bot.get_stats()
                self._send_stats()
                print("Statistics reset")
        except Exception as e:
            print(f"Error resetting stats: {e}")
    
    def _on_bot_status_update(self, message):
        """Callback for bot status updates"""
        self.status['current_activity'] = message
        self._send_status()
    
    def _send_status(self):
        """Send current status to desktop app"""
        if self.bot:
            self.status.update(self.bot.get_status())
        
        # Calculate uptime
        if self.status['start_time']:
            uptime = datetime.now() - self.status['start_time']
            self.status['uptime'] = str(uptime).split('.')[0]
        
        self.status_queue.put(self.status)
    
    def _send_stats(self):
        """Send current statistics to desktop app"""
        if self.bot:
            self.stats.update(self.bot.get_stats())
        
        self.stats_queue.put(self.stats)
    
    def send_command(self, command):
        """Send a command to the bot"""
        self.command_queue.put(command)
    
    def get_status(self):
        """Get current bot status"""
        return self.status.copy()
    
    def get_stats(self):
        """Get current bot statistics"""
        return self.stats.copy()
    
    def is_running(self):
        """Check if bot is running"""
        return self.running

# Main execution for testing
if __name__ == "__main__":
    bridge = ThunderboltBridge()
    
    # Test commands
    print("Testing TSMPoke Thunderbolt Bridge...")
    
    # Start bot
    bridge.send_command({'type': 'start_bot', 'mode': 'catching'})
    time.sleep(2)
    
    # Get status
    bridge.send_command({'type': 'get_status'})
    time.sleep(1)
    
    # Get stats
    bridge.send_command({'type': 'get_stats'})
    time.sleep(1)
    
    # Change mode
    bridge.send_command({'type': 'change_mode', 'mode': 'raiding'})
    time.sleep(2)
    
    # Stop bot
    bridge.send_command({'type': 'stop_bot'})
    time.sleep(1)
    
    print("Bridge test completed!")
