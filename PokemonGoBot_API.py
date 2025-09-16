"""
PokemonGoBot REST API Client
Integrates with the official PokemonGoBot REST API for real Pokemon GO automation
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any

class PokemonGoBotAPI:
    """Client for PokemonGoBot REST API"""
    
    def __init__(self, base_url="http://localhost:8080", bot_name="default", password="", gui_callback=None):
        self.base_url = base_url.rstrip('/')
        self.bot_name = bot_name
        self.password = password
        self.session_token = None
        self.gui_callback = gui_callback
        self.logger = logging.getLogger(__name__)
        
        # API endpoints
        self.endpoints = {
            'auth': f"/api/bot/{bot_name}/auth",
            'start': f"/api/bot/{bot_name}/start",
            'stop': f"/api/bot/{bot_name}/stop",
            'status': f"/api/bot/{bot_name}/status",
            'pokemons': f"/api/bot/{bot_name}/pokemons",
            'profile': f"/api/bot/{bot_name}/profile",
            'pokedex': f"/api/bot/{bot_name}/pokedex",
            'items': f"/api/bot/{bot_name}/items",
            'location': f"/api/bot/{bot_name}/location",
            'use_incense': f"/api/bot/{bot_name}/useIncense",
            'use_lucky_egg': f"/api/bot/{bot_name}/useLuckyEgg",
            'evolve_pokemon': f"/api/bot/{bot_name}/pokemon/{{id}}/evolve",
            'transfer_pokemon': f"/api/bot/{bot_name}/pokemon/{{id}}/transfer",
            'power_up_pokemon': f"/api/bot/{bot_name}/pokemon/{{id}}/powerup"
        }
    
    def _log(self, message):
        """Log message and send to GUI if callback available"""
        self.logger.info(message)
        if self.gui_callback:
            self.gui_callback(message)
    
    def _make_request(self, method, endpoint, data=None, params=None):
        """Make authenticated API request"""
        try:
            url = self.base_url + endpoint
            headers = {'Content-Type': 'application/json'}
            
            # Add authentication token if available
            if self.session_token:
                headers['X-PGB-ACCESS-TOKEN'] = self.session_token
            
            # Make request
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check response
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return response.text
            elif response.status_code == 401:
                self._log("❌ Authentication failed - invalid token")
                self.session_token = None
                return None
            elif response.status_code == 404:
                self._log("❌ Bot not found or API endpoint not available")
                return None
            else:
                self._log(f"❌ API request failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            self._log("❌ Cannot connect to PokemonGoBot API - is the bot running?")
            return None
        except requests.exceptions.Timeout:
            self._log("❌ API request timed out")
            return None
        except Exception as e:
            self._log(f"❌ API request error: {e}")
            return None
    
    def authenticate(self):
        """Authenticate with PokemonGoBot API"""
        try:
            self._log("🔐 Authenticating with PokemonGoBot API...")
            
            # Send password as raw text
            response = requests.post(
                self.base_url + self.endpoints['auth'],
                data=self.password,
                headers={'Content-Type': 'text/plain'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.session_token = response.text.strip()
                self._log("✅ Successfully authenticated with PokemonGoBot API")
                return True
            else:
                self._log(f"❌ Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            self._log("❌ Cannot connect to PokemonGoBot API - make sure the bot is running on port 8080")
            return False
        except Exception as e:
            self._log(f"❌ Authentication error: {e}")
            return False
    
    def start_bot(self):
        """Start the PokemonGoBot"""
        try:
            self._log("🚀 Starting PokemonGoBot...")
            result = self._make_request('POST', self.endpoints['start'])
            if result is not None:
                self._log("✅ PokemonGoBot started successfully")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error starting bot: {e}")
            return False
    
    def stop_bot(self):
        """Stop the PokemonGoBot"""
        try:
            self._log("⏹️ Stopping PokemonGoBot...")
            result = self._make_request('POST', self.endpoints['stop'])
            if result is not None:
                self._log("✅ PokemonGoBot stopped successfully")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error stopping bot: {e}")
            return False
    
    def get_bot_status(self):
        """Get bot status"""
        try:
            result = self._make_request('GET', self.endpoints['status'])
            return result
        except Exception as e:
            self._log(f"❌ Error getting bot status: {e}")
            return None
    
    def get_pokemons(self):
        """Get all Pokemon"""
        try:
            result = self._make_request('GET', self.endpoints['pokemons'])
            return result
        except Exception as e:
            self._log(f"❌ Error getting Pokemon: {e}")
            return None
    
    def get_profile(self):
        """Get player profile"""
        try:
            result = self._make_request('GET', self.endpoints['profile'])
            return result
        except Exception as e:
            self._log(f"❌ Error getting profile: {e}")
            return None
    
    def get_pokedex(self):
        """Get Pokedex data"""
        try:
            result = self._make_request('GET', self.endpoints['pokedex'])
            return result
        except Exception as e:
            self._log(f"❌ Error getting Pokedex: {e}")
            return None
    
    def get_items(self):
        """Get inventory items"""
        try:
            result = self._make_request('GET', self.endpoints['items'])
            return result
        except Exception as e:
            self._log(f"❌ Error getting items: {e}")
            return None
    
    def set_location(self, lat, lng, alt=10):
        """Set bot location"""
        try:
            data = {
                "lat": lat,
                "lng": lng,
                "alt": alt
            }
            result = self._make_request('POST', self.endpoints['location'], data=data)
            if result is not None:
                self._log(f"📍 Location set to: {lat}, {lng}, {alt}")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error setting location: {e}")
            return False
    
    def use_incense(self):
        """Use incense"""
        try:
            result = self._make_request('POST', self.endpoints['use_incense'])
            if result is not None:
                self._log("🕯️ Used incense")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error using incense: {e}")
            return False
    
    def use_lucky_egg(self):
        """Use lucky egg"""
        try:
            result = self._make_request('POST', self.endpoints['use_lucky_egg'])
            if result is not None:
                self._log("🥚 Used lucky egg")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error using lucky egg: {e}")
            return False
    
    def evolve_pokemon(self, pokemon_id):
        """Evolve a Pokemon"""
        try:
            endpoint = self.endpoints['evolve_pokemon'].format(id=pokemon_id)
            result = self._make_request('POST', endpoint)
            if result is not None:
                self._log(f"🔄 Evolving Pokemon {pokemon_id}")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error evolving Pokemon: {e}")
            return False
    
    def transfer_pokemon(self, pokemon_id):
        """Transfer a Pokemon"""
        try:
            endpoint = self.endpoints['transfer_pokemon'].format(id=pokemon_id)
            result = self._make_request('POST', endpoint)
            if result is not None:
                self._log(f"📤 Transferring Pokemon {pokemon_id}")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error transferring Pokemon: {e}")
            return False
    
    def power_up_pokemon(self, pokemon_id):
        """Power up a Pokemon"""
        try:
            endpoint = self.endpoints['power_up_pokemon'].format(id=pokemon_id)
            result = self._make_request('POST', endpoint)
            if result is not None:
                self._log(f"⚡ Powering up Pokemon {pokemon_id}")
                return True
            return False
        except Exception as e:
            self._log(f"❌ Error powering up Pokemon: {e}")
            return False
    
    def get_player_info(self):
        """Get comprehensive player information"""
        try:
            profile = self.get_profile()
            if not profile:
                return None
            
            # Extract player info from profile
            player_info = {
                'level': profile.get('level', 1),
                'experience': profile.get('experience', 0),
                'stardust': profile.get('stardust', 0),
                'team': profile.get('team', 'Unknown'),
                'username': profile.get('username', 'Unknown'),
                'pokemon_caught': profile.get('pokemon_caught', 0),
                'pokestops_visited': profile.get('pokestops_visited', 0),
                'gyms_battled': profile.get('gyms_battled', 0),
                'km_walked': profile.get('km_walked', 0.0)
            }
            
            return player_info
            
        except Exception as e:
            self._log(f"❌ Error getting player info: {e}")
            return None
    
    def get_statistics(self):
        """Get bot statistics"""
        try:
            status = self.get_bot_status()
            if not status:
                return {}
            
            return {
                'current_activity': status.get('current_activity', 'Unknown'),
                'pokemon_caught': status.get('pokemon_caught', 0),
                'pokestops_spun': status.get('pokestops_spun', 0),
                'gyms_battled': status.get('gyms_battled', 0),
                'xp_gained': status.get('xp_gained', 0),
                'stardust_earned': status.get('stardust_earned', 0),
                'shiny_caught': status.get('shiny_caught', 0),
                'perfect_iv_caught': status.get('perfect_iv_caught', 0),
                'raids_completed': status.get('raids_completed', 0)
            }
            
        except Exception as e:
            self._log(f"❌ Error getting statistics: {e}")
            return {}
    
    def is_connected(self):
        """Check if API is connected and authenticated"""
        return self.session_token is not None
    
    def test_connection(self):
        """Test API connection"""
        try:
            if not self.authenticate():
                return False
            
            # Test with a simple API call
            status = self.get_bot_status()
            return status is not None
            
        except Exception as e:
            self._log(f"❌ Connection test failed: {e}")
            return False
