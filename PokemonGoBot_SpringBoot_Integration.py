#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon Go Bot Spring Boot Integration for VexityBot GUI
Integrates the Kotlin/Spring Boot Pokemon Go Bot with the VexityBot GUI system
"""

import json
import requests
import threading
import time
import subprocess
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

class PokemonGoBotSpringBootIntegration:
    """Integration class for Pokemon Go Bot Spring Boot backend with VexityBot GUI"""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.logger = logging.getLogger(__name__)
        
        # Spring Boot configuration
        self.spring_boot_config = {
            'enabled': True,
            'base_url': 'http://localhost:8080',
            'api_endpoint': '/api/bot',
            'auth_endpoint': '/api/bot/{bot_name}/auth',
            'bots_endpoint': '/api/bots',
            'load_endpoint': '/api/bot/{bot_name}/load',
            'unload_endpoint': '/api/bot/{bot_name}/unload',
            'reload_endpoint': '/api/bot/{bot_name}/reload',
            'start_endpoint': '/api/bot/{bot_name}/start',
            'stop_endpoint': '/api/bot/{bot_name}/stop',
            'pokemons_endpoint': '/api/bot/{bot_name}/pokemons',
            'pokemon_transfer_endpoint': '/api/bot/{bot_name}/pokemon/{pokemon_id}/transfer',
            'pokemon_evolve_endpoint': '/api/bot/{bot_name}/pokemon/{pokemon_id}/evolve',
            'pokemon_powerup_endpoint': '/api/bot/{bot_name}/pokemon/{pokemon_id}/powerup',
            'pokemon_favorite_endpoint': '/api/bot/{bot_name}/pokemon/{pokemon_id}/favorite',
            'pokemon_rename_endpoint': '/api/bot/{bot_name}/pokemon/{pokemon_id}/rename',
            'items_endpoint': '/api/bot/{bot_name}/items',
            'item_drop_endpoint': '/api/bot/{bot_name}/item/{item_id}/drop/{quantity}',
            'use_incense_endpoint': '/api/bot/{bot_name}/useIncense',
            'use_lucky_egg_endpoint': '/api/bot/{bot_name}/useLuckyEgg',
            'location_endpoint': '/api/bot/{bot_name}/location',
            'set_location_endpoint': '/api/bot/{bot_name}/location/{latitude}/{longitude}',
            'profile_endpoint': '/api/bot/{bot_name}/profile',
            'pokedex_endpoint': '/api/bot/{bot_name}/pokedex',
            'eggs_endpoint': '/api/bot/{bot_name}/eggs',
            'jar_file': 'PokemonGoBot.jar',
            'config_file': 'config.properties',
            'java_executable': 'java',
            'spring_profile': 'dev',
            'server_port': 8080,
            'auto_start': True,
            'auto_restart': True,
            'restart_delay': 5
        }
        
        # Bot management
        self.bots = {}
        self.active_bots = {}
        self.bot_threads = {}
        self.spring_boot_process = None
        self.is_running = False
        
        # API authentication
        self.api_auth = {}
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'VexityBot-PokemonGoBot-Integration/1.0'
        })
        
        # Bot passwords for authentication
        self.bot_passwords = {}
        
        # Statistics
        self.stats = {
            'total_bots': 0,
            'active_bots': 0,
            'pokemon_caught': 0,
            'pokestops_spun': 0,
            'gyms_battled': 0,
            'raids_completed': 0,
            'xp_gained': 0,
            'stardust_earned': 0,
            'start_time': None,
            'last_update': None
        }
        
        # Initialize Spring Boot if enabled
        if self.spring_boot_config['enabled']:
            self._initialize_spring_boot()
    
    def _initialize_spring_boot(self):
        """Initialize Spring Boot Pokemon Go Bot backend"""
        try:
            self.update_status("🚀 Initializing Pokemon Go Bot Spring Boot backend...")
            
            # Check if Spring Boot is already running
            if self._check_spring_boot_status():
                self.update_status("✅ Spring Boot backend already running")
                return True
            
            # Start Spring Boot application
            if self._start_spring_boot():
                self.update_status("✅ Spring Boot backend started successfully")
                self.is_running = True
                return True
            else:
                self.update_status("❌ Failed to start Spring Boot backend")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Spring Boot initialization error: {e}")
            return False
    
    def _check_spring_boot_status(self):
        """Check if Spring Boot backend is running"""
        try:
            response = self.session.get(f"{self.spring_boot_config['base_url']}/actuator/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _start_spring_boot(self):
        """Start Spring Boot Pokemon Go Bot application"""
        try:
            # Check if JAR file exists
            jar_path = self.spring_boot_config['jar_file']
            if not os.path.exists(jar_path):
                self.update_status(f"❌ JAR file not found: {jar_path}")
                return False
            
            # Prepare Spring Boot command
            cmd = [
                self.spring_boot_config['java_executable'],
                '-jar', jar_path,
                '--server.port=' + str(self.spring_boot_config['server_port']),
                '--spring.profiles.active=' + self.spring_boot_config['spring_profile']
            ]
            
            # Start Spring Boot process
            self.spring_boot_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for Spring Boot to start
            self.update_status("⏳ Waiting for Spring Boot to start...")
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self._check_spring_boot_status():
                    self.update_status("✅ Spring Boot backend is ready!")
                    return True
                self.update_status(f"⏳ Starting... ({i+1}/30)")
            
            self.update_status("❌ Spring Boot failed to start within timeout")
            return False
            
        except Exception as e:
            self.update_status(f"❌ Failed to start Spring Boot: {e}")
            return False
    
    def _stop_spring_boot(self):
        """Stop Spring Boot Pokemon Go Bot application"""
        try:
            if self.spring_boot_process:
                self.spring_boot_process.terminate()
                self.spring_boot_process.wait(timeout=10)
                self.spring_boot_process = None
                self.update_status("✅ Spring Boot backend stopped")
                return True
        except Exception as e:
            self.update_status(f"❌ Error stopping Spring Boot: {e}")
            return False
    
    def create_bot_config(self, bot_name: str, config: Dict[str, Any]) -> bool:
        """Create configuration for a Pokemon Go Bot"""
        try:
            # Default bot configuration
            default_config = {
                'bot_name': bot_name,
                'enabled': True,
                'location': {
                    'lat': 40.7589,  # Times Square, NYC
                    'lng': -73.9851,
                    'alt': 10
                },
                'credentials': {
                    'username': '',
                    'password': '',
                    'auth_type': 'PTC'  # PTC or Google
                },
                'settings': {
                    'walk_speed': 4.16,
                    'catch_pokemon': True,
                    'spin_pokestops': True,
                    'battle_gyms': False,
                    'catch_legendary': True,
                    'catch_shiny': True,
                    'transfer_duplicates': True,
                    'min_cp_threshold': 100,
                    'max_pokemon_storage': 1000
                },
                'advanced': {
                    'human_like_delays': True,
                    'random_movements': True,
                    'smart_timing': True,
                    'ban_bypass': True,
                    'ai_automation': True
                }
            }
            
            # Merge with provided config
            default_config.update(config)
            
            # Save bot configuration
            config_file = f"config/{bot_name}.json"
            os.makedirs("config", exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            self.update_status(f"✅ Bot configuration created: {bot_name}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to create bot config: {e}")
            return False
    
    def authenticate_bot(self, bot_name: str, password: str) -> bool:
        """Authenticate with bot using REST API password"""
        try:
            # Send raw password in request body
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['auth_endpoint'].format(bot_name=bot_name)}",
                data=password,  # Raw data, not JSON
                headers={'Content-Type': 'text/plain'},
                timeout=10
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                token = auth_data.get('token')
                if token:
                    self.api_auth[bot_name] = token
                    self.session.headers['X-PGB-ACCESS-TOKEN'] = token
                    self.update_status(f"✅ Authenticated with bot: {bot_name}")
                    return True
                else:
                    self.update_status(f"❌ No token received for bot: {bot_name}")
                    return False
            else:
                self.update_status(f"❌ Authentication failed for bot {bot_name}: {response.status_code}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Authentication error for {bot_name}: {e}")
            return False
    
    def set_bot_password(self, bot_name: str, password: str):
        """Set password for bot authentication"""
        self.bot_passwords[bot_name] = password
        self.update_status(f"🔐 Password set for bot: {bot_name}")
    
    def register_bot(self, bot_name: str, config: Dict[str, Any] = None) -> bool:
        """Register a new Pokemon Go Bot with Spring Boot backend"""
        try:
            # Create bot configuration
            if not self.create_bot_config(bot_name, config or {}):
                return False
            
            # Generate random password if not provided
            if bot_name not in self.bot_passwords:
                import secrets
                password = secrets.token_urlsafe(16)
                self.bot_passwords[bot_name] = password
                self.update_status(f"🔐 Generated password for bot {bot_name}: {password}")
            
            # Store bot info
            self.bots[bot_name] = {
                'name': bot_name,
                'config_file': f"config/{bot_name}.json",
                'password': self.bot_passwords[bot_name],
                'enabled': True
            }
            self.stats['total_bots'] += 1
            self.update_status(f"✅ Bot registered: {bot_name}")
            return True
                
        except Exception as e:
            self.update_status(f"❌ Bot registration error: {e}")
            return False
    
    def load_bot(self, bot_name: str) -> bool:
        """Load a Pokemon Go Bot"""
        try:
            if bot_name not in self.bots:
                self.update_status(f"❌ Bot not found: {bot_name}")
                return False
            
            # Authenticate first
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['load_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Bot loaded: {bot_name}")
                return True
            else:
                self.update_status(f"❌ Failed to load bot: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Bot load error: {e}")
            return False
    
    def unload_bot(self, bot_name: str) -> bool:
        """Unload a Pokemon Go Bot"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['unload_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Bot unloaded: {bot_name}")
                return True
            else:
                self.update_status(f"❌ Failed to unload bot: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Bot unload error: {e}")
            return False
    
    def reload_bot(self, bot_name: str) -> bool:
        """Reload a Pokemon Go Bot"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['reload_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Bot reloaded: {bot_name}")
                return True
            else:
                self.update_status(f"❌ Failed to reload bot: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Bot reload error: {e}")
            return False
    
    def start_bot(self, bot_name: str) -> bool:
        """Start a Pokemon Go Bot"""
        try:
            if bot_name not in self.bots:
                self.update_status(f"❌ Bot not found: {bot_name}")
                return False
            
            # Authenticate first
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['start_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.active_bots[bot_name] = {
                    'status': 'running',
                    'start_time': datetime.now(),
                    'last_update': datetime.now()
                }
                self.stats['active_bots'] += 1
                self.update_status(f"✅ Bot started: {bot_name}")
                return True
            else:
                self.update_status(f"❌ Failed to start bot: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Bot start error: {e}")
            return False
    
    def stop_bot(self, bot_name: str) -> bool:
        """Stop a Pokemon Go Bot"""
        try:
            if bot_name not in self.active_bots:
                self.update_status(f"❌ Bot not running: {bot_name}")
                return False
            
            # Authenticate first
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['stop_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                del self.active_bots[bot_name]
                self.stats['active_bots'] -= 1
                self.update_status(f"✅ Bot stopped: {bot_name}")
                return True
            else:
                self.update_status(f"❌ Failed to stop bot: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Bot stop error: {e}")
            return False
    
    def _ensure_authenticated(self, bot_name: str) -> bool:
        """Ensure bot is authenticated, authenticate if needed"""
        if bot_name in self.api_auth:
            return True
        
        if bot_name in self.bot_passwords:
            return self.authenticate_bot(bot_name, self.bot_passwords[bot_name])
        
        self.update_status(f"❌ No password set for bot: {bot_name}")
        return False
    
    def get_bot_status(self, bot_name: str) -> Dict[str, Any]:
        """Get status of a specific bot"""
        try:
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['status_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get status: {response.text}'}
                
        except Exception as e:
            return {'error': f'Status request error: {e}'}
    
    def get_bot_data(self, bot_name: str) -> Dict[str, Any]:
        """Get data from a specific bot"""
        try:
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['data_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get data: {response.text}'}
                
        except Exception as e:
            return {'error': f'Data request error: {e}'}
    
    def update_bot_config(self, bot_name: str, config: Dict[str, Any]) -> bool:
        """Update configuration of a bot"""
        try:
            response = self.session.put(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['config_endpoint'].format(bot_name=bot_name)}",
                json=config,
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Bot configuration updated: {bot_name}")
                return True
            else:
                self.update_status(f"❌ Failed to update config: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Config update error: {e}")
            return False
    
    def get_all_bots_status(self) -> Dict[str, Any]:
        """Get status of all bots (no authentication required)"""
        try:
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['bots_endpoint']}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get all bots status: {response.text}'}
                
        except Exception as e:
            return {'error': f'All bots status error: {e}'}
    
    # Pokemon Management Methods
    def get_pokemons(self, bot_name: str) -> Dict[str, Any]:
        """Get all pokemons for a bot"""
        try:
            if not self._ensure_authenticated(bot_name):
                return {'error': 'Authentication failed'}
            
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['pokemons_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get pokemons: {response.text}'}
                
        except Exception as e:
            return {'error': f'Get pokemons error: {e}'}
    
    def transfer_pokemon(self, bot_name: str, pokemon_id: str) -> bool:
        """Transfer a pokemon"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['pokemon_transfer_endpoint'].format(bot_name=bot_name, pokemon_id=pokemon_id)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Pokemon {pokemon_id} transferred")
                return True
            else:
                self.update_status(f"❌ Failed to transfer pokemon: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Transfer pokemon error: {e}")
            return False
    
    def evolve_pokemon(self, bot_name: str, pokemon_id: str) -> bool:
        """Evolve a pokemon"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['pokemon_evolve_endpoint'].format(bot_name=bot_name, pokemon_id=pokemon_id)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Pokemon {pokemon_id} evolved")
                return True
            elif response.status_code == 400:
                self.update_status(f"❌ Not enough candy to evolve pokemon {pokemon_id}")
                return False
            else:
                self.update_status(f"❌ Failed to evolve pokemon: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Evolve pokemon error: {e}")
            return False
    
    def powerup_pokemon(self, bot_name: str, pokemon_id: str) -> bool:
        """Power up a pokemon"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['pokemon_powerup_endpoint'].format(bot_name=bot_name, pokemon_id=pokemon_id)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Pokemon {pokemon_id} powered up")
                return True
            elif response.status_code == 400:
                self.update_status(f"❌ Not enough candy or stardust to power up pokemon {pokemon_id}")
                return False
            else:
                self.update_status(f"❌ Failed to power up pokemon: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Power up pokemon error: {e}")
            return False
    
    def toggle_pokemon_favorite(self, bot_name: str, pokemon_id: str) -> bool:
        """Toggle favorite for a pokemon"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['pokemon_favorite_endpoint'].format(bot_name=bot_name, pokemon_id=pokemon_id)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Pokemon {pokemon_id} favorite toggled")
                return True
            else:
                self.update_status(f"❌ Failed to toggle pokemon favorite: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Toggle pokemon favorite error: {e}")
            return False
    
    def rename_pokemon(self, bot_name: str, pokemon_id: str, new_name: str) -> bool:
        """Rename a pokemon"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['pokemon_rename_endpoint'].format(bot_name=bot_name, pokemon_id=pokemon_id)}",
                data=new_name,  # Raw data, not JSON
                headers={'Content-Type': 'text/plain'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Pokemon {pokemon_id} renamed to {new_name}")
                return True
            else:
                self.update_status(f"❌ Failed to rename pokemon: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Rename pokemon error: {e}")
            return False
    
    # Item Management Methods
    def get_items(self, bot_name: str) -> Dict[str, Any]:
        """Get all items for a bot"""
        try:
            if not self._ensure_authenticated(bot_name):
                return {'error': 'Authentication failed'}
            
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['items_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get items: {response.text}'}
                
        except Exception as e:
            return {'error': f'Get items error: {e}'}
    
    def drop_item(self, bot_name: str, item_id: str, quantity: int) -> bool:
        """Drop quantity of an item"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.delete(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['item_drop_endpoint'].format(bot_name=bot_name, item_id=item_id, quantity=quantity)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Dropped {quantity} of item {item_id}")
                return True
            elif response.status_code == 400:
                self.update_status(f"❌ Invalid quantity for item {item_id}")
                return False
            else:
                self.update_status(f"❌ Failed to drop item: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Drop item error: {e}")
            return False
    
    def use_incense(self, bot_name: str) -> bool:
        """Use an incense"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['use_incense_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Incense used for bot {bot_name}")
                return True
            elif response.status_code == 400:
                self.update_status(f"❌ Not enough incense for bot {bot_name}")
                return False
            else:
                self.update_status(f"❌ Failed to use incense: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Use incense error: {e}")
            return False
    
    def use_lucky_egg(self, bot_name: str) -> bool:
        """Use a lucky egg"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['use_lucky_egg_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Lucky egg used for bot {bot_name}")
                return True
            elif response.status_code == 400:
                self.update_status(f"❌ Not enough lucky eggs for bot {bot_name}")
                return False
            else:
                self.update_status(f"❌ Failed to use lucky egg: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Use lucky egg error: {e}")
            return False
    
    # Location and Profile Methods
    def get_location(self, bot_name: str) -> Dict[str, Any]:
        """Get bot current location"""
        try:
            if not self._ensure_authenticated(bot_name):
                return {'error': 'Authentication failed'}
            
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['location_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get location: {response.text}'}
                
        except Exception as e:
            return {'error': f'Get location error: {e}'}
    
    def set_location(self, bot_name: str, latitude: float, longitude: float) -> bool:
        """Change bot location"""
        try:
            if not self._ensure_authenticated(bot_name):
                return False
            
            response = self.session.post(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['set_location_endpoint'].format(bot_name=bot_name, latitude=latitude, longitude=longitude)}",
                timeout=10
            )
            
            if response.status_code == 200:
                self.update_status(f"✅ Location set to {latitude}, {longitude} for bot {bot_name}")
                return True
            elif response.status_code == 400:
                self.update_status(f"❌ Invalid latitude or longitude: {latitude}, {longitude}")
                return False
            else:
                self.update_status(f"❌ Failed to set location: {response.text}")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Set location error: {e}")
            return False
    
    def get_profile(self, bot_name: str) -> Dict[str, Any]:
        """Get account profile"""
        try:
            if not self._ensure_authenticated(bot_name):
                return {'error': 'Authentication failed'}
            
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['profile_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get profile: {response.text}'}
                
        except Exception as e:
            return {'error': f'Get profile error: {e}'}
    
    def get_pokedex(self, bot_name: str) -> Dict[str, Any]:
        """Get account pokedex"""
        try:
            if not self._ensure_authenticated(bot_name):
                return {'error': 'Authentication failed'}
            
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['pokedex_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get pokedex: {response.text}'}
                
        except Exception as e:
            return {'error': f'Get pokedex error: {e}'}
    
    def get_eggs(self, bot_name: str) -> Dict[str, Any]:
        """Get eggs"""
        try:
            if not self._ensure_authenticated(bot_name):
                return {'error': 'Authentication failed'}
            
            response = self.session.get(
                f"{self.spring_boot_config['base_url']}{self.spring_boot_config['eggs_endpoint'].format(bot_name=bot_name)}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'Failed to get eggs: {response.text}'}
                
        except Exception as e:
            return {'error': f'Get eggs error: {e}'}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        try:
            # Get statistics from all active bots
            total_stats = {
                'pokemon_caught': 0,
                'pokestops_spun': 0,
                'gyms_battled': 0,
                'raids_completed': 0,
                'xp_gained': 0,
                'stardust_earned': 0
            }
            
            for bot_name in self.active_bots:
                bot_data = self.get_bot_data(bot_name)
                if 'error' not in bot_data:
                    for key in total_stats:
                        total_stats[key] += bot_data.get(key, 0)
            
            # Update local stats
            self.stats.update(total_stats)
            self.stats['last_update'] = datetime.now()
            
            return self.stats
            
        except Exception as e:
            self.update_status(f"❌ Statistics error: {e}")
            return self.stats
    
    def start_all_bots(self) -> bool:
        """Start all registered bots"""
        try:
            success_count = 0
            total_bots = len(self.bots)
            
            for bot_name in self.bots:
                if self.start_bot(bot_name):
                    success_count += 1
            
            self.update_status(f"✅ Started {success_count}/{total_bots} bots")
            return success_count > 0
            
        except Exception as e:
            self.update_status(f"❌ Start all bots error: {e}")
            return False
    
    def stop_all_bots(self) -> bool:
        """Stop all active bots"""
        try:
            success_count = 0
            total_bots = len(self.active_bots)
            
            for bot_name in list(self.active_bots.keys()):
                if self.stop_bot(bot_name):
                    success_count += 1
            
            self.update_status(f"✅ Stopped {success_count}/{total_bots} bots")
            return success_count > 0
            
        except Exception as e:
            self.update_status(f"❌ Stop all bots error: {e}")
            return False
    
    def restart_spring_boot(self) -> bool:
        """Restart Spring Boot backend"""
        try:
            self.update_status("🔄 Restarting Spring Boot backend...")
            
            # Stop current instance
            self._stop_spring_boot()
            time.sleep(self.spring_boot_config['restart_delay'])
            
            # Start new instance
            if self._start_spring_boot():
                self.update_status("✅ Spring Boot backend restarted successfully")
                return True
            else:
                self.update_status("❌ Failed to restart Spring Boot backend")
                return False
                
        except Exception as e:
            self.update_status(f"❌ Restart error: {e}")
            return False
    
    def update_status(self, message: str):
        """Update status and notify GUI"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        status_message = f"{timestamp} - {message}"
        
        if self.gui_callback:
            self.gui_callback(status_message)
        
        self.logger.info(message)
        print(status_message)
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return {
            'spring_boot_running': self._check_spring_boot_status(),
            'total_bots': len(self.bots),
            'active_bots': len(self.active_bots),
            'integration_enabled': self.spring_boot_config['enabled'],
            'base_url': self.spring_boot_config['base_url'],
            'last_update': self.stats['last_update']
        }
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.update_status("🧹 Cleaning up Pokemon Go Bot integration...")
            
            # Stop all bots
            self.stop_all_bots()
            
            # Stop Spring Boot
            self._stop_spring_boot()
            
            self.update_status("✅ Cleanup completed")
            
        except Exception as e:
            self.update_status(f"❌ Cleanup error: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create integration instance
    integration = PokemonGoBotSpringBootIntegration()
    
    # Test integration
    print("Testing Pokemon Go Bot Spring Boot Integration...")
    print("=" * 60)
    
    # Test Spring Boot status
    print("1. Checking Spring Boot status...")
    status = integration.get_integration_status()
    print(f"   Spring Boot running: {status['spring_boot_running']}")
    print(f"   Integration enabled: {status['integration_enabled']}")
    
    # Test bot registration
    print("\n2. Testing bot registration...")
    test_config = {
        'credentials': {
            'username': 'test_user',
            'password': 'test_pass',
            'auth_type': 'PTC'
        },
        'location': {
            'lat': 40.7589,
            'lng': -73.9851,
            'alt': 10
        }
    }
    
    if integration.register_bot('test_bot', test_config):
        print("   ✅ Bot registered successfully")
    else:
        print("   ❌ Bot registration failed")
    
    # Test bot management
    print("\n3. Testing bot management...")
    if integration.start_bot('test_bot'):
        print("   ✅ Bot started successfully")
        
        # Get bot status
        bot_status = integration.get_bot_status('test_bot')
        print(f"   Bot status: {bot_status}")
        
        # Stop bot
        if integration.stop_bot('test_bot'):
            print("   ✅ Bot stopped successfully")
    else:
        print("   ❌ Bot start failed")
    
    # Test statistics
    print("\n4. Testing statistics...")
    stats = integration.get_statistics()
    print(f"   Total bots: {stats['total_bots']}")
    print(f"   Active bots: {stats['active_bots']}")
    
    # Cleanup
    print("\n5. Cleaning up...")
    integration.cleanup()
    
    print("\n" + "=" * 60)
    print("Pokemon Go Bot Spring Boot Integration Test Completed!")
    print("=" * 60)
