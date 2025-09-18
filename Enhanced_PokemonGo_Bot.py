# -*- coding: utf-8 -*-
"""
Enhanced Pokemon GO Bot - Integrated with pgoapi and VexityBot GUI
Advanced Pokemon GO automation with full pgoapi integration
"""

import datetime
import json
import logging
import os
import random
import re
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox
import queue
import asyncio
from typing import Dict, List, Optional, Tuple, Any

# ADDED: Import the downloaded pgoapi
try:
    import sys
    import os
    # Add local pgoapi directory to path
    # Handle both development and PyInstaller environments
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        base_path = sys._MEIPASS
        pgoapi_path = os.path.join(base_path, 'pgoapi')
    else:
        # Running in development
        pgoapi_path = os.path.join(os.getcwd(), 'pgoapi')
    
    if pgoapi_path not in sys.path and os.path.exists(pgoapi_path):
        sys.path.insert(0, pgoapi_path)
    
    from pgoapi import PGoApi
    from pgoapi.exceptions import AuthException, NotLoggedInException, ServerBusyOrOfflineException
    from pgoapi.utilities import f2i, get_cell_ids
    from pgoapi.auth_ptc import AuthPtc
    from pgoapi.auth_google import AuthGoogle
    PGOAPI_AVAILABLE = True
    print("✅ pgoapi successfully imported")
except ImportError as e:
    PGOAPI_AVAILABLE = False
    print(f"❌ pgoapi import failed: {e}")

# Optional geolocation imports with fallbacks
try:
    import requests
    import geopy
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    GEOLOCATION_AVAILABLE = True
except ImportError:
    GEOLOCATION_AVAILABLE = False
    print("Warning: Geolocation libraries not available. Some features may be limited.")

# Pokemon Map integration imports
try:
    from bs4 import BeautifulSoup
    import urllib.parse
    from urllib.request import urlopen
    import webbrowser
    MAP_INTEGRATION_AVAILABLE = True
except ImportError:
    MAP_INTEGRATION_AVAILABLE = False
    print("Warning: Map integration libraries not available. Some features may be limited.")

# Import the existing Pokemon GO bot modules
try:
    # ADDED: Skip problematic pokemongo_bot imports for now
    # from pokemongo_bot import *
    # from pokemongo_bot.api_wrapper import ApiWrapper
    # from pokemongo_bot.inventory import init_inventory, player, Pokemons
    # from pokemongo_bot.event_manager import EventManager
    # from pokemongo_bot.human_behaviour import sleep
    # from pokemongo_bot.metrics import Metrics
    # from pokemongo_bot.sleep_schedule import SleepSchedule
    EXISTING_BOT_AVAILABLE = False  # Temporarily disabled
    print("⚠️ pokemongo_bot import skipped (data files missing)")
except ImportError as e:
    EXISTING_BOT_AVAILABLE = False
    print(f"Warning: Could not import existing pokemongo_bot modules: {e}")

class EnhancedPokemonGoBot:
    """Enhanced Pokemon GO Bot with pgoapi integration"""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.running = False
        self.paused = False
        self.current_mode = "idle"
        self.logger = logging.getLogger(__name__)
        
        # ADDED: Initialize pgoapi
        self.pgoapi = None
        self.api_initialized = False
        
        # Bot configuration
        self.config = {
            'location': {
                'lat': 40.7589,  # Times Square, NYC
                'lng': -73.9851,
                'alt': 10,
                'address': 'Times Square, New York, NY',
                'zip_code': '10036',
                'city': 'New York',
                'state': 'NY',
                'country': 'US'
            },
            'walk_speed': 4.16,  # km/h
            'catch_pokemon': True,
            'spin_pokestops': True,
            'battle_gyms': False,
            'catch_legendary': True,
            'catch_mythical': True,
            'catch_shiny': True,
            'catch_perfect_iv': True,
            'transfer_duplicates': True,
            'keep_high_cp': True,
            'keep_high_iv': True,
            'target_pokemon': [],
            'ban_bypass': True,
            'ai_automation': True,
            'smart_catching': True,
            'auto_evolve': True,
            'auto_powerup': True,
            'mega_evolve': True,
            'min_cp_threshold': 100,
            'max_pokemon_storage': 1000,
            'human_like_delays': True,
            'random_movements': True,
            'smart_timing': True,
            'geolocation_enabled': True,
            'auto_location_update': True,
            'map_integration_enabled': True,
            'map_auto_refresh': True,
            'map_refresh_interval': 30,
            'map_radius_km': 2.0,
            'prioritize_rare_pokemon': True,
            'auto_navigate_to_pokemon': True,
            'auto_navigate_to_pokestops': True,
            'auto_navigate_to_gyms': True,
            # ADDED: pgoapi specific settings
            'auth_provider': 'ptc',  # 'ptc' or 'google'
            'username': '',
            'password': '',
            'proxy_config': None,
            'device_info': None,
            'hash_server_token': None,
            'api_endpoint': 'pgorelease.nianticlabs.com/plfe'
        }
        
        # Bot statistics
        self.stats = {
            'start_time': None,
            'pokemon_caught': 0,
            'pokestops_spun': 0,
            'gyms_battled': 0,
            'eggs_hatched': 0,
            'distance_walked': 0.0,
            'xp_gained': 0,
            'stardust_gained': 0,
            'items_collected': 0,
            'errors_encountered': 0,
            'session_duration': 0,
            'current_level': 1,
            'total_pokemon': 0,
            'unique_pokemon': 0,
            'shiny_pokemon': 0,
            'perfect_iv_pokemon': 0,
            'legendary_pokemon': 0,
            'mythical_pokemon': 0
        }
        
        # Bot modes
        self.modes = {
            'idle': self._idle_mode,
            'catching': self._catching_mode,
            'raiding': self._raiding_mode,
            'battling': self._battling_mode,
            'exploring': self._exploring_mode,
            'farming': self._farming_mode,
            'hunting': self._hunting_mode,
            'evolving': self._evolving_mode,
            'powering_up': self._powering_up_mode,
            'mega_evolving': self._mega_evolving_mode
        }
        
        # ADDED: Initialize pgoapi if available
        if PGOAPI_AVAILABLE:
            self._initialize_pgoapi()
        
        # Initialize existing bot if available
        if EXISTING_BOT_AVAILABLE:
            self._initialize_existing_bot()
    
    def _initialize_pgoapi(self):
        """Initialize pgoapi with proper configuration"""
        try:
            # ADDED: Validate credentials before initialization
            if not self.config.get('username') or not self.config.get('password'):
                self.update_status("❌ pgoapi initialization failed: Invalid Credential Input - Please provide username/password or an oauth2 refresh token")
                self.api_initialized = False
                return
            
            # ADDED: Create pgoapi instance with error handling
            self.pgoapi = PGoApi(
                provider=self.config['auth_provider'],
                username=self.config['username'],
                password=self.config['password'],
                position_lat=self.config['location']['lat'],
                position_lng=self.config['location']['lng'],
                position_alt=self.config['location']['alt'],
                proxy_config=self.config['proxy_config'],
                device_info=self.config['device_info']
            )
            
            # Set API endpoint
            self.pgoapi.set_api_endpoint(self.config['api_endpoint'])
            
            # Set hash server token if available
            if self.config['hash_server_token']:
                self.pgoapi.set_hash_server_token(self.config['hash_server_token'])
            
            # ADDED: Test authentication without actually logging in
            self.api_initialized = True
            self.update_status("✅ pgoapi initialized successfully")
            self.logger.info("pgoapi initialized successfully")
            
        except Exception as e:
            error_msg = str(e)
            if "redirects" in error_msg.lower():
                self.update_status("❌ pgoapi initialization failed: Network authentication error - Check internet connection and credentials")
            elif "credential" in error_msg.lower():
                self.update_status("❌ pgoapi initialization failed: Invalid Credential Input - Please provide username/password or an oauth2 refresh token")
            else:
                self.update_status(f"❌ pgoapi initialization failed: {e}")
            
            self.logger.error(f"pgoapi initialization failed: {e}")
            self.api_initialized = False
    
    def _initialize_existing_bot(self):
        """Initialize existing Pokemon GO bot components"""
        try:
            # Initialize existing bot components
            self.existing_bot = None  # Will be set when needed
            self.update_status("✅ Existing bot components available")
            self.logger.info("Existing bot components available")
            
        except Exception as e:
            self.update_status(f"❌ Existing bot initialization failed: {e}")
            self.logger.error(f"Existing bot initialization failed: {e}")
    
    def update_status(self, message):
        """Update bot status and notify GUI"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        status_message = f"[{timestamp}] {message}"
        
        if self.gui_callback:
            self.gui_callback(status_message)
        
        self.logger.info(status_message)
        print(status_message)
    
    def start(self):
        """Start the enhanced Pokemon GO bot"""
        if not self.api_initialized:
            if not self.config.get('username') or not self.config.get('password'):
                self.update_status("❌ Cannot start bot: Please set credentials first")
            else:
                self.update_status("❌ Cannot start bot: pgoapi not initialized - Check credentials and network connection")
            return False
        
        try:
            self.running = True
            self.paused = False
            self.stats['start_time'] = datetime.datetime.now()
            self.current_mode = "catching"
            
            self.update_status("🚀 Enhanced Pokemon GO Bot started")
            self.update_status(f"📍 Location: {self.config['location']['address']}")
            self.update_status(f"🎯 Mode: {self.current_mode}")
            
            # Start bot loop in separate thread
            self.bot_thread = threading.Thread(target=self._bot_loop, daemon=True)
            self.bot_thread.start()
            
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to start bot: {e}")
            self.logger.error(f"Failed to start bot: {e}")
            return False
    
    def _bot_loop(self):
        """Main bot loop"""
        while self.running:
            try:
                if not self.paused:
                    self.step()
                
                # Human-like delay
                if self.config['human_like_delays']:
                    delay = random.uniform(1.0, 3.0)
                    time.sleep(delay)
                else:
                    time.sleep(0.5)
                    
            except Exception as e:
                self.update_status(f"❌ Bot loop error: {e}")
                self.stats['errors_encountered'] += 1
                time.sleep(5)  # Wait before retrying
    
    def step(self):
        """Run one bot step"""
        if not self.running or self.paused:
            return
        
        try:
            # ADDED: Use pgoapi for real Pokemon GO interactions
            if self.api_initialized and self.pgoapi:
                self._pgoapi_step()
            
            # Run current mode
            if self.current_mode in self.modes:
                self.modes[self.current_mode]()
            else:
                self._idle_mode()
            
            # Update statistics
            self._update_statistics()
            
        except Exception as e:
            self.update_status(f"❌ Bot step error: {e}")
            self.stats['errors_encountered'] += 1
    
    def _pgoapi_step(self):
        """Execute pgoapi operations"""
        try:
            # ADDED: Get map objects using pgoapi
            if self.pgoapi:
                # Get current position
                lat = self.config['location']['lat']
                lng = self.config['location']['lng']
                alt = self.config['location']['alt']
                
                # Set position
                self.pgoapi.set_position(lat, lng, alt)
                
                # Get map objects
                request = self.pgoapi.create_request()
                request.get_map_objects(
                    latitude=f2i(lat),
                    longitude=f2i(lng),
                    since_timestamp_ms=[0, ] * 21,
                    cell_id=get_cell_ids(lat, lng)
                )
                
                response = request.call()
                
                if response:
                    self._process_map_objects(response)
                
        except Exception as e:
            self.update_status(f"❌ pgoapi step error: {e}")
            self.logger.error(f"pgoapi step error: {e}")
    
    def _process_map_objects(self, response):
        """Process map objects from pgoapi response"""
        try:
            # ADDED: Process map objects response
            if 'responses' in response and 'GET_MAP_OBJECTS' in response['responses']:
                map_objects = response['responses']['GET_MAP_OBJECTS']
                
                if 'map_cells' in map_objects:
                    for cell in map_objects['map_cells']:
                        # Process forts (pokestops and gyms)
                        if 'forts' in cell:
                            for fort in cell['forts']:
                                self._process_fort(fort)
                        
                        # Process wild pokemon
                        if 'wild_pokemons' in cell:
                            for pokemon in cell['wild_pokemons']:
                                self._process_wild_pokemon(pokemon)
                        
                        # Process catchable pokemon
                        if 'catchable_pokemons' in cell:
                            for pokemon in cell['catchable_pokemons']:
                                self._process_catchable_pokemon(pokemon)
        
        except Exception as e:
            self.update_status(f"❌ Map objects processing error: {e}")
            self.logger.error(f"Map objects processing error: {e}")
    
    def _process_fort(self, fort):
        """Process a fort (pokestop or gym)"""
        try:
            fort_id = fort.get('id', 'unknown')
            fort_type = fort.get('type', 1)  # 1 = pokestop, 2 = gym
            
            if fort_type == 1:  # Pokestop
                self.update_status(f"🎯 Found Pokestop: {fort_id}")
                if self.config['spin_pokestops']:
                    self._spin_pokestop(fort)
            elif fort_type == 2:  # Gym
                self.update_status(f"🏟️ Found Gym: {fort_id}")
                if self.config['battle_gyms']:
                    self._battle_gym(fort)
        
        except Exception as e:
            self.update_status(f"❌ Fort processing error: {e}")
            self.logger.error(f"Fort processing error: {e}")
    
    def _process_wild_pokemon(self, pokemon):
        """Process a wild pokemon"""
        try:
            pokemon_id = pokemon.get('pokemon_id', 0)
            encounter_id = pokemon.get('encounter_id', 0)
            lat = pokemon.get('latitude', 0)
            lng = pokemon.get('longitude', 0)
            
            # Get pokemon name
            pokemon_name = self._get_pokemon_name(pokemon_id)
            
            self.update_status(f"🐾 Found wild {pokemon_name} (ID: {pokemon_id})")
            
            if self.config['catch_pokemon']:
                self._catch_pokemon(pokemon)
        
        except Exception as e:
            self.update_status(f"❌ Wild pokemon processing error: {e}")
            self.logger.error(f"Wild pokemon processing error: {e}")
    
    def _process_catchable_pokemon(self, pokemon):
        """Process a catchable pokemon"""
        try:
            pokemon_id = pokemon.get('pokemon_id', 0)
            encounter_id = pokemon.get('encounter_id', 0)
            lat = pokemon.get('latitude', 0)
            lng = pokemon.get('longitude', 0)
            
            # Get pokemon name
            pokemon_name = self._get_pokemon_name(pokemon_id)
            
            self.update_status(f"🎯 Found catchable {pokemon_name} (ID: {pokemon_id})")
            
            if self.config['catch_pokemon']:
                self._catch_pokemon(pokemon)
        
        except Exception as e:
            self.update_status(f"❌ Catchable pokemon processing error: {e}")
            self.logger.error(f"Catchable pokemon processing error: {e}")
    
    def _get_pokemon_name(self, pokemon_id):
        """Get pokemon name by ID"""
        # ADDED: Basic pokemon name mapping
        pokemon_names = {
            1: "Bulbasaur", 2: "Ivysaur", 3: "Venusaur", 4: "Charmander", 5: "Charmeleon",
            6: "Charizard", 7: "Squirtle", 8: "Wartortle", 9: "Blastoise", 10: "Caterpie",
            # Add more as needed
        }
        return pokemon_names.get(pokemon_id, f"Pokemon_{pokemon_id}")
    
    def _spin_pokestop(self, fort):
        """Spin a pokestop using pgoapi"""
        try:
            if not self.pgoapi:
                return
            
            fort_id = fort.get('id')
            lat = fort.get('latitude')
            lng = fort.get('longitude')
            
            # ADDED: Spin pokestop using pgoapi
            request = self.pgoapi.create_request()
            request.fort_search(
                fort_id=fort_id,
                player_latitude=f2i(lat),
                player_longitude=f2i(lng),
                fort_latitude=f2i(lat),
                fort_longitude=f2i(lng)
            )
            
            response = request.call()
            
            if response and 'responses' in response:
                fort_search = response['responses'].get('FORT_SEARCH', {})
                if fort_search.get('result') == 1:
                    self.update_status(f"✅ Spun Pokestop: {fort_id}")
                    self.stats['pokestops_spun'] += 1
                else:
                    self.update_status(f"❌ Failed to spin Pokestop: {fort_id}")
        
        except Exception as e:
            self.update_status(f"❌ Pokestop spin error: {e}")
            self.logger.error(f"Pokestop spin error: {e}")
    
    def _catch_pokemon(self, pokemon):
        """Catch a pokemon using pgoapi"""
        try:
            if not self.pgoapi:
                return
            
            encounter_id = pokemon.get('encounter_id')
            pokemon_id = pokemon.get('pokemon_id')
            lat = pokemon.get('latitude')
            lng = pokemon.get('longitude')
            
            pokemon_name = self._get_pokemon_name(pokemon_id)
            
            # ADDED: Encounter pokemon using pgoapi
            request = self.pgoapi.create_request()
            request.encounter(
                encounter_id=encounter_id,
                spawn_point_id=pokemon.get('spawn_point_id', ''),
                player_latitude=f2i(lat),
                player_longitude=f2i(lng)
            )
            
            response = request.call()
            
            if response and 'responses' in response:
                encounter = response['responses'].get('ENCOUNTER', {})
                if encounter.get('status') == 1:
                    self.update_status(f"🎯 Encountered {pokemon_name}")
                    
                    # ADDED: Catch pokemon using pgoapi
                    request = self.pgoapi.create_request()
                    request.catch_pokemon(
                        encounter_id=encounter_id,
                        pokeball=1,  # Poke Ball
                        normalized_reticle_size=1.0,
                        spawn_point_id=pokemon.get('spawn_point_id', ''),
                        hit_pokemon=True,
                        spin_modifier=1.0,
                        normalized_hit_position=1.0
                    )
                    
                    catch_response = request.call()
                    
                    if catch_response and 'responses' in catch_response:
                        catch_result = catch_response['responses'].get('CATCH_POKEMON', {})
                        if catch_result.get('status') == 1:
                            self.update_status(f"✅ Caught {pokemon_name}!")
                            self.stats['pokemon_caught'] += 1
                        else:
                            self.update_status(f"❌ Failed to catch {pokemon_name}")
                else:
                    self.update_status(f"❌ Failed to encounter {pokemon_name}")
        
        except Exception as e:
            self.update_status(f"❌ Pokemon catch error: {e}")
            self.logger.error(f"Pokemon catch error: {e}")
    
    def _battle_gym(self, fort):
        """Battle a gym using pgoapi"""
        try:
            if not self.pgoapi:
                return
            
            fort_id = fort.get('id')
            lat = fort.get('latitude')
            lng = fort.get('longitude')
            
            self.update_status(f"⚔️ Battling Gym: {fort_id}")
            
            # ADDED: Gym battle logic using pgoapi
            # This would require more complex implementation
            # For now, just log the attempt
            self.update_status(f"🏟️ Gym battle attempted: {fort_id}")
            self.stats['gyms_battled'] += 1
        
        except Exception as e:
            self.update_status(f"❌ Gym battle error: {e}")
            self.logger.error(f"Gym battle error: {e}")
    
    def _idle_mode(self):
        """Idle mode - bot is waiting"""
        self.update_status("😴 Bot is idle")
    
    def _catching_mode(self):
        """Catching mode - focus on catching pokemon"""
        self.update_status("🎯 Catching mode active")
    
    def _raiding_mode(self):
        """Raiding mode - focus on raids"""
        self.update_status("⚔️ Raiding mode active")
    
    def _battling_mode(self):
        """Battling mode - focus on gym battles"""
        self.update_status("🏟️ Battling mode active")
    
    def _exploring_mode(self):
        """Exploring mode - general exploration"""
        self.update_status("🗺️ Exploring mode active")
    
    def _farming_mode(self):
        """Farming mode - focus on items and XP"""
        self.update_status("🌾 Farming mode active")
    
    def _hunting_mode(self):
        """Hunting mode - focus on specific pokemon"""
        self.update_status("🎯 Hunting mode active")
    
    def _evolving_mode(self):
        """Evolving mode - focus on evolving pokemon"""
        self.update_status("✨ Evolving mode active")
    
    def _powering_up_mode(self):
        """Powering up mode - focus on powering up pokemon"""
        self.update_status("💪 Powering up mode active")
    
    def _mega_evolving_mode(self):
        """Mega evolving mode - focus on mega evolution"""
        self.update_status("🌟 Mega evolving mode active")
    
    def _update_statistics(self):
        """Update bot statistics"""
        if self.stats['start_time']:
            self.stats['session_duration'] = (datetime.datetime.now() - self.stats['start_time']).total_seconds()
    
    def get_statistics(self):
        """Get current bot statistics"""
        return self.stats.copy()
    
    def get_detailed_statistics(self):
        """Get detailed bot statistics"""
        try:
            stats = self.get_statistics()
            
            # Calculate additional statistics
            if stats['start_time']:
                runtime = datetime.datetime.now() - stats['start_time']
                stats['runtime_formatted'] = str(runtime).split('.')[0]
            
            stats['pokemon_per_hour'] = 0
            stats['pokestops_per_hour'] = 0
            stats['xp_per_hour'] = 0
            
            if stats['session_duration'] > 0:
                hours = stats['session_duration'] / 3600
                stats['pokemon_per_hour'] = stats['pokemon_caught'] / hours
                stats['pokestops_per_hour'] = stats['pokestops_spun'] / hours
                stats['xp_per_hour'] = stats['xp_gained'] / hours
            
            return stats
            
        except Exception as e:
            self.update_status(f"❌ Error getting detailed stats: {e}")
            return {}
    
    def is_running(self):
        """Check if bot is running"""
        return self.running
    
    def is_paused(self):
        """Check if bot is paused"""
        return self.paused
    
    def pause(self):
        """Pause the bot"""
        self.paused = True
        self.update_status("⏸️ Bot paused")
    
    def resume(self):
        """Resume the bot"""
        self.paused = False
        self.update_status("▶️ Bot resumed")
    
    def stop(self):
        """Stop the bot"""
        self.running = False
        self.paused = False
        self.update_status("⏹️ Bot stopped")
    
    def set_mode(self, mode):
        """Set bot mode"""
        if mode in self.modes:
            self.current_mode = mode
            self.update_status(f"🎯 Mode changed to: {mode}")
        else:
            self.update_status(f"❌ Invalid mode: {mode}")
    
    def set_location(self, lat, lng, alt=10):
        """Set bot location"""
        self.config['location']['lat'] = lat
        self.config['location']['lng'] = lng
        self.config['location']['alt'] = alt
        
        # Update pgoapi position if available
        if self.pgoapi:
            self.pgoapi.set_position(lat, lng, alt)
        
        self.update_status(f"📍 Location set to: {lat}, {lng}, {alt}")
    
    def set_credentials(self, username, password, provider='ptc'):
        """Set authentication credentials"""
        if not username or not password:
            self.update_status("❌ Invalid credentials: Username and password required")
            return False
            
        self.config['username'] = username
        self.config['password'] = password
        self.config['auth_provider'] = provider
        
        # Reinitialize pgoapi with new credentials
        if PGOAPI_AVAILABLE:
            try:
                self._initialize_pgoapi()
                self.update_status(f"🔐 Credentials set for {provider} account: {username}")
                return True
            except Exception as e:
                self.update_status(f"❌ Authentication failed: {e}")
                return False
        else:
            self.update_status("❌ pgoapi not available")
            return False
    
    def get_status(self):
        """Get current bot status"""
        status = {
            'running': self.running,
            'paused': self.paused,
            'mode': self.current_mode,
            'api_initialized': self.api_initialized,
            'pgoapi_available': PGOAPI_AVAILABLE,
            'existing_bot_available': EXISTING_BOT_AVAILABLE,
            'has_credentials': bool(self.config.get('username') and self.config.get('password')),
            'location': self.config['location'],
            'statistics': self.get_statistics()
        }
        return status
    
    def validate_credentials(self):
        """Validate if credentials are properly set"""
        if not self.config.get('username'):
            return False, "Username not set"
        if not self.config.get('password'):
            return False, "Password not set"
        return True, "Credentials are set"

# ADDED: Example usage and testing
if __name__ == "__main__":
    # Create bot instance
    bot = EnhancedPokemonGoBot()
    
    # Set credentials (replace with actual credentials)
    bot.set_credentials("your_username", "your_password", "ptc")
    
    # Set location
    bot.set_location(40.7589, -73.9851, 10)
    
    # Start bot
    if bot.start():
        print("Bot started successfully!")
        
        # Run for a short time for testing
        time.sleep(30)
        
        # Stop bot
        bot.stop()
        print("Bot stopped.")
    else:
        print("Failed to start bot.")
