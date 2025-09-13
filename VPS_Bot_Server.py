#!/usr/bin/env python3

"""
VPS Bot Server - Runs ShadowStrike OSRS Bot on VPS
Handles client connections and bot control remotely
"""

import socket
import threading
import json
import time
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import queue
import pickle

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ShadowStrike_OSRS_Bot import ShadowStrikeOSRSBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vps_bot_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VPSBotServer:
    """VPS Server that runs the OSRS bot and handles client connections"""
    
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.bot = None
        self.bot_thread = None
        self.is_running = False
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
        # Bot status tracking
        self.bot_status = {
            'running': False,
            'phase': 'ACCOUNT_CREATION',
            'current_activity': 'Starting',
            'stats': {},
            'last_update': datetime.now()
        }
        
        logger.info("VPS Bot Server initialized")
    
    def start_server(self):
        """Start the VPS server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.is_running = True
            logger.info(f"VPS Bot Server started on {self.host}:{self.port}")
            
            # Start bot status updater
            status_thread = threading.Thread(target=self.update_bot_status, daemon=True)
            status_thread.start()
            
            # Start command processor
            command_thread = threading.Thread(target=self.process_commands, daemon=True)
            command_thread.start()
            
            # Accept client connections
            while self.is_running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logger.info(f"Client connected from {client_address}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as e:
                    if self.is_running:
                        logger.error(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            self.stop_server()
    
    def stop_server(self):
        """Stop the VPS server"""
        self.is_running = False
        
        # Stop bot if running
        if self.bot and self.bot.is_running:
            self.bot.is_running = False
        
        # Close all client connections
        for client_socket in self.clients.values():
            try:
                client_socket.close()
            except:
                pass
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        logger.info("VPS Bot Server stopped")
    
    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        client_id = f"{client_address[0]}:{client_address[1]}"
        self.clients[client_id] = client_socket
        
        try:
            while self.is_running:
                # Receive command from client
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    command = json.loads(data.decode('utf-8'))
                    logger.info(f"Received command from {client_id}: {command['action']}")
                    
                    # Process command
                    response = self.process_command(command)
                    
                    # Send response back to client
                    response_data = json.dumps(response).encode('utf-8')
                    client_socket.send(response_data)
                    
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from {client_id}")
                    error_response = {
                        'success': False,
                        'error': 'Invalid JSON format'
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                
                except Exception as e:
                    logger.error(f"Error processing command from {client_id}: {e}")
                    error_response = {
                        'success': False,
                        'error': str(e)
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
        
        except Exception as e:
            logger.error(f"Client {client_id} error: {e}")
        
        finally:
            # Remove client from list
            if client_id in self.clients:
                del self.clients[client_id]
            client_socket.close()
            logger.info(f"Client {client_id} disconnected")
    
    def process_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Process command from client"""
        action = command.get('action')
        
        try:
            if action == 'start_bot':
                return self.start_bot()
            elif action == 'stop_bot':
                return self.stop_bot()
            elif action == 'get_status':
                return self.get_bot_status()
            elif action == 'get_stats':
                return self.get_bot_stats()
            elif action == 'send_command':
                return self.send_bot_command(command.get('bot_command', ''))
            elif action == 'get_logs':
                return self.get_bot_logs()
            elif action == 'restart_bot':
                return self.restart_bot()
            elif action == 'ping':
                return {'success': True, 'message': 'pong', 'timestamp': datetime.now().isoformat()}
            else:
                return {
                    'success': False,
                    'error': f'Unknown action: {action}'
                }
        
        except Exception as e:
            logger.error(f"Error processing command {action}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def start_bot(self) -> Dict[str, Any]:
        """Start the OSRS bot"""
        try:
            if self.bot and self.bot.is_running:
                return {
                    'success': False,
                    'error': 'Bot is already running'
                }
            
            # Create new bot instance
            self.bot = ShadowStrikeOSRSBot()
            
            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            
            self.bot_status['running'] = True
            self.bot_status['last_update'] = datetime.now()
            
            logger.info("OSRS Bot started")
            return {
                'success': True,
                'message': 'Bot started successfully',
                'bot_status': self.bot_status
            }
        
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def stop_bot(self) -> Dict[str, Any]:
        """Stop the OSRS bot"""
        try:
            if not self.bot or not self.bot.is_running:
                return {
                    'success': False,
                    'error': 'Bot is not running'
                }
            
            # Stop bot
            self.bot.is_running = False
            
            # Wait for bot thread to finish
            if self.bot_thread and self.bot_thread.is_alive():
                self.bot_thread.join(timeout=5)
            
            self.bot_status['running'] = False
            self.bot_status['last_update'] = datetime.now()
            
            logger.info("OSRS Bot stopped")
            return {
                'success': True,
                'message': 'Bot stopped successfully',
                'bot_status': self.bot_status
            }
        
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_bot(self):
        """Run the OSRS bot (called in separate thread)"""
        try:
            if self.bot:
                self.bot.run()
        except Exception as e:
            logger.error(f"Bot execution error: {e}")
            self.bot_status['running'] = False
        finally:
            self.bot_status['running'] = False
            self.bot_status['last_update'] = datetime.now()
    
    def get_bot_status(self) -> Dict[str, Any]:
        """Get current bot status"""
        try:
            if self.bot:
                self.bot_status.update({
                    'phase': self.bot.stats.phase.name,
                    'current_activity': self.bot.current_activity,
                    'current_location': self.bot.current_location,
                    'stats': {
                        'skills': self.bot.stats.skills,
                        'gp': self.bot.stats.gp,
                        'combat_level': self.bot.stats.combat_level,
                        'total_level': self.bot.stats.total_level,
                        'deaths': self.bot.stats.deaths,
                        'bans': self.bot.stats.bans,
                        'quests_completed': len(self.bot.stats.quests_completed)
                    }
                })
            
            return {
                'success': True,
                'bot_status': self.bot_status
            }
        
        except Exception as e:
            logger.error(f"Error getting bot status: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_bot_stats(self) -> Dict[str, Any]:
        """Get detailed bot statistics"""
        try:
            if not self.bot:
                return {
                    'success': False,
                    'error': 'Bot not initialized'
                }
            
            stats = {
                'phase': self.bot.stats.phase.name,
                'skills': self.bot.stats.skills,
                'gp': self.bot.stats.gp,
                'combat_level': self.bot.stats.combat_level,
                'total_level': self.bot.stats.total_level,
                'deaths': self.bot.stats.deaths,
                'bans': self.bot.stats.bans,
                'quests_completed': self.bot.stats.quests_completed,
                'start_time': self.bot.stats.start_time.isoformat(),
                'current_location': self.bot.current_location,
                'current_activity': self.bot.current_activity,
                'is_running': self.bot.is_running
            }
            
            return {
                'success': True,
                'stats': stats
            }
        
        except Exception as e:
            logger.error(f"Error getting bot stats: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_bot_command(self, command: str) -> Dict[str, Any]:
        """Send command to bot"""
        try:
            if not self.bot:
                return {
                    'success': False,
                    'error': 'Bot not initialized'
                }
            
            # Add command to queue
            self.command_queue.put(command)
            
            return {
                'success': True,
                'message': f'Command "{command}" queued for bot'
            }
        
        except Exception as e:
            logger.error(f"Error sending bot command: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_bot_logs(self) -> Dict[str, Any]:
        """Get bot logs"""
        try:
            log_file = 'shadowstrike_bot.log'
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = f.readlines()
                    # Return last 100 lines
                    recent_logs = logs[-100:] if len(logs) > 100 else logs
                
                return {
                    'success': True,
                    'logs': recent_logs
                }
            else:
                return {
                    'success': True,
                    'logs': ['No logs available']
                }
        
        except Exception as e:
            logger.error(f"Error getting bot logs: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def restart_bot(self) -> Dict[str, Any]:
        """Restart the bot"""
        try:
            # Stop bot if running
            if self.bot and self.bot.is_running:
                self.bot.is_running = False
                if self.bot_thread and self.bot_thread.is_alive():
                    self.bot_thread.join(timeout=5)
            
            # Start bot again
            return self.start_bot()
        
        except Exception as e:
            logger.error(f"Error restarting bot: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_bot_status(self):
        """Update bot status periodically"""
        while self.is_running:
            try:
                if self.bot:
                    self.bot_status.update({
                        'running': self.bot.is_running,
                        'phase': self.bot.stats.phase.name,
                        'current_activity': self.bot.current_activity,
                        'current_location': self.bot.current_location,
                        'last_update': datetime.now()
                    })
                
                time.sleep(1)  # Update every second
            
            except Exception as e:
                logger.error(f"Error updating bot status: {e}")
                time.sleep(5)
    
    def process_commands(self):
        """Process commands from queue"""
        while self.is_running:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get(timeout=1)
                    logger.info(f"Processing bot command: {command}")
                    
                    # Process command here if needed
                    # For now, just log it
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing command: {e}")

def main():
    """Main function to start VPS server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='VPS Bot Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=9999, help='Port to bind to')
    
    args = parser.parse_args()
    
    server = VPSBotServer(host=args.host, port=args.port)
    
    try:
        logger.info("Starting VPS Bot Server...")
        server.start_server()
    except KeyboardInterrupt:
        logger.info("Shutting down VPS Bot Server...")
        server.stop_server()
    except Exception as e:
        logger.error(f"Server error: {e}")
        server.stop_server()

if __name__ == "__main__":
    main()
