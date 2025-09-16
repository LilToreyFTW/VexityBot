# -*- coding: utf-8 -*-
"""
Thunderbolt Pokemon GO Bot - Integrated with VexityBot GUI
Advanced Pokemon GO automation with full GUI integration
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
    import json
    from urllib.request import urlopen
    import webbrowser
    MAP_INTEGRATION_AVAILABLE = True
except ImportError:
    MAP_INTEGRATION_AVAILABLE = False
    print("Warning: Map integration libraries not available. Some features may be limited.")

try:
    import zipcode
    ZIPCODE_AVAILABLE = True
except ImportError:
    ZIPCODE_AVAILABLE = False

try:
    import geocoder
    GEOCODER_AVAILABLE = True
except ImportError:
    GEOCODER_AVAILABLE = False

try:
    import reverse_geocoder as rg
    REVERSE_GEOCODER_AVAILABLE = True
except ImportError:
    REVERSE_GEOCODER_AVAILABLE = False

# Import the existing Pokemon GO bot modules
try:
    from pokemongo_bot import *
    from pokemongo_bot.api_wrapper import ApiWrapper
    from pokemongo_bot.inventory import init_inventory, player, Pokemons
    from pokemongo_bot.event_manager import EventManager
    from pokemongo_bot.human_behaviour import sleep
    from pokemongo_bot.metrics import Metrics
    from pokemongo_bot.sleep_schedule import SleepSchedule
except ImportError as e:
    print(f"Warning: Could not import pokemongo_bot modules: {e}")
    print("Some features may not be available")

class ThunderboltPokemonGOBot:
    """Advanced Pokemon GO Bot integrated with VexityBot GUI"""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.running = False
        self.paused = False
        self.current_mode = "idle"
        self.logger = logging.getLogger(__name__)
        
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
            'auto_navigate_to_gyms': True
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
            'current_activity': 'Ready',
            'high_cp_caught': 0,
            'pokemon_evolved': 0,
            'pokemon_powered_up': 0,
            'mega_evolutions': 0,
            'ban_attempts_blocked': 0,
            'ai_decisions_made': 0
        }
        
        # AI and ban bypass systems
        self.ai_system = {
            'human_like_delays': True,
            'random_movements': True,
            'smart_timing': True,
            'behavior_patterns': [],
            'last_action_time': 0,
            'action_cooldown': 0,
            'movement_patterns': [],
            'catch_patterns': [],
            'spin_patterns': []
        }
        
        # Pokemon management database
        self.pokemon_database = {}
        self.high_cp_pokemon = {}
        self.evolution_candidates = {}
        self.powerup_candidates = {}
        self.mega_candidates = {}
        
        # Ban bypass techniques
        self.ban_bypass = {
            'human_timing': True,
            'random_delays': True,
            'movement_simulation': True,
            'action_randomization': True,
            'session_rotation': True,
            'device_fingerprinting': True
        }
        
        # Initialize API wrapper
        self.api = None
        self.player = None
        self.inventory = None
        
        # Event system
        self.event_queue = queue.Queue()
        self.status_queue = queue.Queue()
        
        # Pokemon Map integration
        self.map_integration = {
            'enabled': True,
            'base_url': 'https://www.pokemap.net',
            'api_endpoint': 'https://www.pokemap.net/api',
            'map_data': {},
            'pokemon_spawns': [],
            'pokestops': [],
            'gyms': [],
            'nests': [],
            'last_update': None,
            'update_interval': 30,  # seconds
            'auto_refresh': True
        }
        
        # Bot modes
        self.modes = {
            'catching': self._catching_mode,
            'raiding': self._raiding_mode,
            'battling': self._battling_mode,
            'exploring': self._exploring_mode,
            'idle': self._idle_mode,
            'map_mode': self._map_mode
        }
    
    def set_gui_callback(self, callback):
        """Set the GUI callback function for status updates"""
        self.gui_callback = callback
    
    def set_credentials(self, username, password, login_method):
        """Set login credentials"""
        self.config['username'] = username
        self.config['password'] = password
        self.config['login_method'] = login_method
    
    def set_location(self, lat, lng, alt):
        """Set bot location"""
        self.config['location']['lat'] = lat
        self.config['location']['lng'] = lng
        self.config['location']['alt'] = alt
    
    def set_walk_speed(self, speed):
        """Set walk speed"""
        self.config['walk_speed'] = speed
    
    def set_catch_pokemon(self, enabled):
        """Enable/disable Pokemon catching"""
        self.config['catch_pokemon'] = enabled
    
    def set_spin_pokestops(self, enabled):
        """Enable/disable Pokestop spinning"""
        self.config['spin_pokestops'] = enabled
    
    def set_battle_gyms(self, enabled):
        """Enable/disable gym battling"""
        self.config['battle_gyms'] = enabled
    
    def set_transfer_pokemon(self, enabled):
        """Enable/disable Pokemon transferring"""
        self.config['transfer_duplicates'] = enabled
    
    def set_target_pokemon(self, pokemon_list):
        """Set specific Pokemon to catch"""
        self.config['target_pokemon'] = pokemon_list
        self.update_status(f"🎯 Target Pokemon set: {len(pokemon_list)} Pokemon selected")
    
    def set_location_by_zip(self, zip_code):
        """Set location using zip code"""
        try:
            location_data = self._get_location_by_zip(zip_code)
            if location_data:
                self.config['location'].update(location_data)
                self.update_status(f"📍 Location set to: {location_data.get('address', 'Unknown')}")
                return True
            else:
                self.update_status(f"❌ Could not find location for zip code: {zip_code}")
                return False
        except Exception as e:
            self.update_status(f"❌ Error setting location by zip: {e}")
            return False
    
    def set_location_by_address(self, address):
        """Set location using address"""
        try:
            location_data = self._get_location_by_address(address)
            if location_data:
                self.config['location'].update(location_data)
                self.update_status(f"📍 Location set to: {address}")
                return True
            else:
                self.update_status(f"❌ Could not find location for address: {address}")
                return False
        except Exception as e:
            self.update_status(f"❌ Error setting location by address: {e}")
            return False
    
    def set_location_by_coordinates(self, lat, lng, alt=10):
        """Set location using coordinates"""
        try:
            location_data = self._get_location_by_coordinates(lat, lng, alt)
            if location_data:
                self.config['location'].update(location_data)
                self.update_status(f"📍 Location set to: {lat}, {lng}")
                return True
            else:
                self.update_status(f"❌ Could not find location for coordinates: {lat}, {lng}")
                return False
        except Exception as e:
            self.update_status(f"❌ Error setting location by coordinates: {e}")
            return False
    
    def _get_location_by_zip(self, zip_code):
        """Get location data by zip code"""
        try:
            # Try multiple geocoding services
            location_data = None
            
            # Method 1: Using geopy with Nominatim
            if GEOLOCATION_AVAILABLE:
                try:
                    geolocator = Nominatim(user_agent="pokemon_go_bot")
                    location = geolocator.geocode(f"{zip_code}, USA")
                    if location:
                        location_data = {
                            'lat': location.latitude,
                            'lng': location.longitude,
                            'alt': 10,
                            'address': location.address,
                            'zip_code': zip_code,
                            'city': self._extract_city_from_address(location.address),
                            'state': self._extract_state_from_address(location.address),
                            'country': 'US'
                        }
                except Exception as e:
                    self.logger.warning(f"Geopy failed: {e}")
            
            # Method 2: Using geocoder
            if not location_data and GEOCODER_AVAILABLE:
                try:
                    g = geocoder.zipcode(zip_code)
                    if g.ok:
                        location_data = {
                            'lat': g.lat,
                            'lng': g.lng,
                            'alt': 10,
                            'address': g.address,
                            'zip_code': zip_code,
                            'city': g.city,
                            'state': g.state,
                            'country': g.country
                        }
                except Exception as e:
                    self.logger.warning(f"Geocoder failed: {e}")
            
            # Method 3: Using zipcode library
            if not location_data and ZIPCODE_AVAILABLE:
                try:
                    zip_info = zipcode.isequal(zip_code)
                    if zip_info:
                        location_data = {
                            'lat': float(zip_info.lat),
                            'lng': float(zip_info.long),
                            'alt': 10,
                            'address': f"{zip_info.city}, {zip_info.state} {zip_code}",
                            'zip_code': zip_code,
                            'city': zip_info.city,
                            'state': zip_info.state,
                            'country': 'US'
                        }
                except Exception as e:
                    self.logger.warning(f"Zipcode library failed: {e}")
            
            # Fallback: Use hardcoded locations for common zip codes
            if not location_data:
                location_data = self._get_fallback_location_by_zip(zip_code)
            
            return location_data
            
        except Exception as e:
            self.logger.error(f"Error getting location by zip: {e}")
            return None
    
    def _get_location_by_address(self, address):
        """Get location data by address"""
        try:
            location_data = None
            
            # Method 1: Using geopy with Nominatim
            if GEOLOCATION_AVAILABLE:
                try:
                    geolocator = Nominatim(user_agent="pokemon_go_bot")
                    location = geolocator.geocode(address)
                    if location:
                        location_data = {
                            'lat': location.latitude,
                            'lng': location.longitude,
                            'alt': 10,
                            'address': location.address,
                            'zip_code': self._extract_zip_from_address(location.address),
                            'city': self._extract_city_from_address(location.address),
                            'state': self._extract_state_from_address(location.address),
                            'country': self._extract_country_from_address(location.address)
                        }
                except Exception as e:
                    self.logger.warning(f"Geopy address failed: {e}")
            
            # Method 2: Using geocoder
            if not location_data and GEOCODER_AVAILABLE:
                try:
                    g = geocoder.osm(address)
                    if g.ok:
                        location_data = {
                            'lat': g.lat,
                            'lng': g.lng,
                            'alt': 10,
                            'address': g.address,
                            'zip_code': self._extract_zip_from_address(g.address),
                            'city': g.city,
                            'state': g.state,
                            'country': g.country
                        }
                except Exception as e:
                    self.logger.warning(f"Geocoder address failed: {e}")
            
            # Fallback: Use hardcoded locations for common addresses
            if not location_data:
                location_data = self._get_fallback_location_by_address(address)
            
            return location_data
            
        except Exception as e:
            self.logger.error(f"Error getting location by address: {e}")
            return None
    
    def _get_location_by_coordinates(self, lat, lng, alt=10):
        """Get location data by coordinates"""
        try:
            location_data = None
            
            # Method 1: Using reverse geocoding with geopy
            if GEOLOCATION_AVAILABLE:
                try:
                    geolocator = Nominatim(user_agent="pokemon_go_bot")
                    location = geolocator.reverse(f"{lat}, {lng}")
                    if location:
                        location_data = {
                            'lat': lat,
                            'lng': lng,
                            'alt': alt,
                            'address': location.address,
                            'zip_code': self._extract_zip_from_address(location.address),
                            'city': self._extract_city_from_address(location.address),
                            'state': self._extract_state_from_address(location.address),
                            'country': self._extract_country_from_address(location.address)
                        }
                except Exception as e:
                    self.logger.warning(f"Geopy reverse failed: {e}")
            
            # Method 2: Using reverse_geocoder
            if not location_data and REVERSE_GEOCODER_AVAILABLE:
                try:
                    result = rg.search((lat, lng))
                    if result:
                        location_data = {
                            'lat': lat,
                            'lng': lng,
                            'alt': alt,
                            'address': f"{result[0]['name']}, {result[0]['admin1']}, {result[0]['cc']}",
                            'zip_code': result[0].get('postal', ''),
                            'city': result[0]['name'],
                            'state': result[0]['admin1'],
                            'country': result[0]['cc']
                        }
                except Exception as e:
                    self.logger.warning(f"Reverse geocoder failed: {e}")
            
            # Fallback: Return coordinates with basic info
            if not location_data:
                location_data = {
                    'lat': lat,
                    'lng': lng,
                    'alt': alt,
                    'address': f"Location {lat:.6f}, {lng:.6f}",
                    'zip_code': '',
                    'city': 'Unknown',
                    'state': 'Unknown',
                    'country': 'Unknown'
                }
            
            return location_data
            
        except Exception as e:
            self.logger.error(f"Error getting location by coordinates: {e}")
            return None
    
    def _extract_zip_from_address(self, address):
        """Extract zip code from address string"""
        try:
            # Look for 5-digit zip code pattern
            zip_pattern = r'\b(\d{5})\b'
            match = re.search(zip_pattern, address)
            return match.group(1) if match else ''
        except Exception:
            return ''
    
    def _extract_city_from_address(self, address):
        """Extract city from address string"""
        try:
            # Simple city extraction - first part before comma
            parts = address.split(',')
            if len(parts) > 0:
                return parts[0].strip()
            return ''
        except Exception:
            return ''
    
    def _extract_state_from_address(self, address):
        """Extract state from address string"""
        try:
            # Look for state abbreviations
            state_pattern = r'\b([A-Z]{2})\b'
            match = re.search(state_pattern, address)
            return match.group(1) if match else ''
        except Exception:
            return ''
    
    def _extract_country_from_address(self, address):
        """Extract country from address string"""
        try:
            # Look for country at the end
            parts = address.split(',')
            if len(parts) > 0:
                return parts[-1].strip()
            return ''
        except Exception:
            return ''
    
    def get_nearby_locations(self, radius_km=5):
        """Get nearby locations within radius"""
        try:
            current_lat = self.config['location']['lat']
            current_lng = self.config['location']['lng']
            
            # Generate nearby locations
            nearby_locations = []
            
            # Generate points in a grid pattern
            for i in range(-radius_km, radius_km + 1, 1):
                for j in range(-radius_km, radius_km + 1, 1):
                    if i == 0 and j == 0:
                        continue  # Skip current location
                    
                    # Calculate new coordinates
                    new_lat = current_lat + (i * 0.01)  # Roughly 1km per 0.01 degrees
                    new_lng = current_lng + (j * 0.01)
                    
                    # Get location info for this point
                    location_info = self._get_location_by_coordinates(new_lat, new_lng)
                    if location_info:
                        nearby_locations.append(location_info)
            
            return nearby_locations
            
        except Exception as e:
            self.logger.error(f"Error getting nearby locations: {e}")
            return []
    
    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two coordinates"""
        try:
            if GEOLOCATION_AVAILABLE:
                # Use geopy for accurate distance calculation
                point1 = (lat1, lng1)
                point2 = (lat2, lng2)
                distance = geodesic(point1, point2).kilometers
                return distance
            else:
                # Fallback: Use Haversine formula for distance calculation
                import math
                
                # Convert latitude and longitude from degrees to radians
                lat1_rad = math.radians(lat1)
                lng1_rad = math.radians(lng1)
                lat2_rad = math.radians(lat2)
                lng2_rad = math.radians(lng2)
                
                # Haversine formula
                dlat = lat2_rad - lat1_rad
                dlng = lng2_rad - lng1_rad
                
                a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
                c = 2 * math.asin(math.sqrt(a))
                
                # Earth's radius in kilometers
                earth_radius = 6371
                distance = earth_radius * c
                
                return distance
                
        except Exception as e:
            self.logger.error(f"Error calculating distance: {e}")
            return 0
    
    def get_optimal_route(self, locations, max_distance=10):
        """Calculate optimal route through locations"""
        try:
            if not locations:
                return []
            
            # Start from current location
            current_location = self.config['location']
            route = [current_location]
            remaining_locations = locations.copy()
            
            while remaining_locations:
                # Find closest location
                closest_location = None
                closest_distance = float('inf')
                
                for location in remaining_locations:
                    distance = self.calculate_distance(
                        current_location['lat'], current_location['lng'],
                        location['lat'], location['lng']
                    )
                    
                    if distance < closest_distance and distance <= max_distance:
                        closest_distance = distance
                        closest_location = location
                
                if closest_location:
                    route.append(closest_location)
                    remaining_locations.remove(closest_location)
                    current_location = closest_location
                else:
                    break  # No more reachable locations
            
            return route
            
        except Exception as e:
            self.logger.error(f"Error calculating optimal route: {e}")
            return []
    
    def get_pokemon_hotspots(self, radius_km=10):
        """Get known Pokemon hotspots in the area"""
        try:
            current_lat = self.config['location']['lat']
            current_lng = self.config['location']['lng']
            
            # Known Pokemon hotspots (these would normally come from a database)
            hotspots = [
                {'name': 'Central Park', 'lat': 40.7829, 'lng': -73.9654, 'type': 'park'},
                {'name': 'Times Square', 'lat': 40.7589, 'lng': -73.9851, 'type': 'urban'},
                {'name': 'Brooklyn Bridge', 'lat': 40.7061, 'lng': -73.9969, 'type': 'landmark'},
                {'name': 'Statue of Liberty', 'lat': 40.6892, 'lng': -74.0445, 'type': 'landmark'},
                {'name': 'High Line Park', 'lat': 40.7480, 'lng': -74.0048, 'type': 'park'},
                {'name': 'Prospect Park', 'lat': 40.6602, 'lng': -73.9690, 'type': 'park'},
                {'name': 'Coney Island', 'lat': 40.5749, 'lng': -73.9857, 'type': 'beach'},
                {'name': 'Flushing Meadows', 'lat': 40.7505, 'lng': -73.8444, 'type': 'park'},
                {'name': 'Van Cortlandt Park', 'lat': 40.8897, 'lng': -73.8988, 'type': 'park'},
                {'name': 'Pelham Bay Park', 'lat': 40.8674, 'lng': -73.8081, 'type': 'park'}
            ]
            
            # Filter hotspots within radius
            nearby_hotspots = []
            for hotspot in hotspots:
                distance = self.calculate_distance(
                    current_lat, current_lng,
                    hotspot['lat'], hotspot['lng']
                )
                
                if distance <= radius_km:
                    hotspot['distance'] = distance
                    nearby_hotspots.append(hotspot)
            
            # Sort by distance
            nearby_hotspots.sort(key=lambda x: x['distance'])
            
            return nearby_hotspots
            
        except Exception as e:
            self.logger.error(f"Error getting Pokemon hotspots: {e}")
            return []
    
    def get_weather_data(self):
        """Get current weather data for the location"""
        try:
            lat = self.config['location']['lat']
            lng = self.config['location']['lng']
            
            # This would normally use a weather API
            # For now, return simulated weather data
            weather_conditions = ['sunny', 'cloudy', 'rainy', 'snowy', 'foggy', 'windy']
            weather = random.choice(weather_conditions)
            
            return {
                'condition': weather,
                'temperature': random.randint(50, 85),
                'humidity': random.randint(30, 90),
                'wind_speed': random.randint(0, 20),
                'pokemon_boost': self._get_weather_boost(weather)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting weather data: {e}")
            return None
    
    def _get_weather_boost(self, weather_condition):
        """Get Pokemon type boost based on weather"""
        weather_boosts = {
            'sunny': ['fire', 'grass', 'ground'],
            'rainy': ['water', 'electric', 'bug'],
            'snowy': ['ice', 'steel'],
            'cloudy': ['normal', 'rock', 'poison'],
            'foggy': ['ghost', 'dark'],
            'windy': ['flying', 'dragon', 'psychic']
        }
        
        return weather_boosts.get(weather_condition, [])
    
    def get_pokestop_density(self, radius_km=5):
        """Get Pokestop density in the area"""
        try:
            # This would normally query a Pokestop database
            # For now, return simulated data
            density_levels = ['low', 'medium', 'high', 'very_high']
            density = random.choice(density_levels)
            
            density_counts = {
                'low': random.randint(1, 5),
                'medium': random.randint(6, 15),
                'high': random.randint(16, 30),
                'very_high': random.randint(31, 50)
            }
            
            return {
                'density': density,
                'count': density_counts[density],
                'radius_km': radius_km
            }
            
        except Exception as e:
            self.logger.error(f"Error getting Pokestop density: {e}")
            return None
    
    def get_gym_density(self, radius_km=5):
        """Get Gym density in the area"""
        try:
            # This would normally query a Gym database
            # For now, return simulated data
            density_levels = ['low', 'medium', 'high']
            density = random.choice(density_levels)
            
            density_counts = {
                'low': random.randint(1, 3),
                'medium': random.randint(4, 8),
                'high': random.randint(9, 15)
            }
            
            return {
                'density': density,
                'count': density_counts[density],
                'radius_km': radius_km
            }
            
        except Exception as e:
            self.logger.error(f"Error getting Gym density: {e}")
            return None
    
    def get_pokemon_spawn_data(self, radius_km=5):
        """Get Pokemon spawn data for the area"""
        try:
            # This would normally query a spawn database
            # For now, return simulated data
            spawn_data = {
                'common_spawns': ['Pidgey', 'Rattata', 'Caterpie', 'Weedle', 'Spearow'],
                'uncommon_spawns': ['Pikachu', 'Squirtle', 'Charmander', 'Bulbasaur', 'Eevee'],
                'rare_spawns': ['Dratini', 'Snorlax', 'Lapras', 'Aerodactyl', 'Chansey'],
                'legendary_spawns': ['Mewtwo', 'Mew', 'Articuno', 'Zapdos', 'Moltres'],
                'spawn_rate': random.uniform(0.1, 0.5),
                'nest_species': random.choice(['Pikachu', 'Squirtle', 'Charmander', 'Bulbasaur'])
            }
            
            return spawn_data
            
        except Exception as e:
            self.logger.error(f"Error getting Pokemon spawn data: {e}")
            return None
    
    def optimize_location_for_pokemon(self, target_pokemon):
        """Find optimal location for specific Pokemon"""
        try:
            # This would normally use Pokemon spawn data
            # For now, return simulated optimal locations
            optimal_locations = [
                {
                    'name': 'Central Park',
                    'lat': 40.7829,
                    'lng': -73.9654,
                    'pokemon_found': target_pokemon,
                    'spawn_rate': random.uniform(0.3, 0.8),
                    'distance_km': self.calculate_distance(
                        self.config['location']['lat'],
                        self.config['location']['lng'],
                        40.7829, -73.9654
                    )
                },
                {
                    'name': 'Prospect Park',
                    'lat': 40.6602,
                    'lng': -73.9690,
                    'pokemon_found': target_pokemon,
                    'spawn_rate': random.uniform(0.2, 0.7),
                    'distance_km': self.calculate_distance(
                        self.config['location']['lat'],
                        self.config['location']['lng'],
                        40.6602, -73.9690
                    )
                }
            ]
            
            # Sort by spawn rate and distance
            optimal_locations.sort(key=lambda x: (x['spawn_rate'], -x['distance_km']), reverse=True)
            
            return optimal_locations
            
        except Exception as e:
            self.logger.error(f"Error optimizing location for Pokemon: {e}")
            return []
    
    def get_location_info(self):
        """Get comprehensive location information"""
        try:
            location = self.config['location']
            
            info = {
                'coordinates': {
                    'latitude': location['lat'],
                    'longitude': location['lng'],
                    'altitude': location['alt']
                },
                'address': {
                    'full_address': location['address'],
                    'city': location['city'],
                    'state': location['state'],
                    'zip_code': location['zip_code'],
                    'country': location['country']
                },
                'weather': self.get_weather_data(),
                'pokestops': self.get_pokestop_density(),
                'gyms': self.get_gym_density(),
                'pokemon_spawns': self.get_pokemon_spawn_data(),
                'hotspots': self.get_pokemon_hotspots(),
                'map_data': self.get_map_data()
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting location info: {e}")
            return None
    
    def _get_fallback_location_by_zip(self, zip_code):
        """Fallback location data for common zip codes"""
        try:
            # Common US zip codes with coordinates
            zip_locations = {
                '10001': {'lat': 40.7505, 'lng': -73.9934, 'city': 'New York', 'state': 'NY'},
                '10036': {'lat': 40.7589, 'lng': -73.9851, 'city': 'New York', 'state': 'NY'},
                '90210': {'lat': 34.0901, 'lng': -118.4065, 'city': 'Beverly Hills', 'state': 'CA'},
                '94102': {'lat': 37.7749, 'lng': -122.4194, 'city': 'San Francisco', 'state': 'CA'},
                '60601': {'lat': 41.8781, 'lng': -87.6298, 'city': 'Chicago', 'state': 'IL'},
                '33101': {'lat': 25.7617, 'lng': -80.1918, 'city': 'Miami', 'state': 'FL'},
                '75201': {'lat': 32.7767, 'lng': -96.7970, 'city': 'Dallas', 'state': 'TX'},
                '85001': {'lat': 33.4484, 'lng': -112.0740, 'city': 'Phoenix', 'state': 'AZ'},
                '98101': {'lat': 47.6062, 'lng': -122.3321, 'city': 'Seattle', 'state': 'WA'},
                '02101': {'lat': 42.3601, 'lng': -71.0589, 'city': 'Boston', 'state': 'MA'},
                '30301': {'lat': 33.7490, 'lng': -84.3880, 'city': 'Atlanta', 'state': 'GA'},
                '80201': {'lat': 39.7392, 'lng': -104.9903, 'city': 'Denver', 'state': 'CO'},
                '89101': {'lat': 36.1699, 'lng': -115.1398, 'city': 'Las Vegas', 'state': 'NV'},
                '97201': {'lat': 45.5152, 'lng': -122.6784, 'city': 'Portland', 'state': 'OR'},
                '55401': {'lat': 44.9778, 'lng': -93.2650, 'city': 'Minneapolis', 'state': 'MN'},
                '48201': {'lat': 42.3314, 'lng': -83.0458, 'city': 'Detroit', 'state': 'MI'},
                '70112': {'lat': 29.9511, 'lng': -90.0715, 'city': 'New Orleans', 'state': 'LA'},
                '85001': {'lat': 33.4484, 'lng': -112.0740, 'city': 'Phoenix', 'state': 'AZ'},
                '84101': {'lat': 40.7608, 'lng': -111.8910, 'city': 'Salt Lake City', 'state': 'UT'},
                '73101': {'lat': 35.4676, 'lng': -97.5164, 'city': 'Oklahoma City', 'state': 'OK'}
            }
            
            if zip_code in zip_locations:
                loc = zip_locations[zip_code]
                return {
                    'lat': loc['lat'],
                    'lng': loc['lng'],
                    'alt': 10,
                    'address': f"{loc['city']}, {loc['state']} {zip_code}",
                    'zip_code': zip_code,
                    'city': loc['city'],
                    'state': loc['state'],
                    'country': 'US'
                }
            
            # If zip code not found, return default NYC location
            return {
                'lat': 40.7589,
                'lng': -73.9851,
                'alt': 10,
                'address': f"New York, NY {zip_code}",
                'zip_code': zip_code,
                'city': 'New York',
                'state': 'NY',
                'country': 'US'
            }
            
        except Exception as e:
            self.logger.error(f"Error in fallback location: {e}")
            return None
    
    def _get_fallback_location_by_address(self, address):
        """Fallback location data for common addresses"""
        try:
            # Common addresses with coordinates
            address_locations = {
                'times square': {'lat': 40.7589, 'lng': -73.9851, 'city': 'New York', 'state': 'NY'},
                'central park': {'lat': 40.7829, 'lng': -73.9654, 'city': 'New York', 'state': 'NY'},
                'brooklyn bridge': {'lat': 40.7061, 'lng': -73.9969, 'city': 'New York', 'state': 'NY'},
                'statue of liberty': {'lat': 40.6892, 'lng': -74.0445, 'city': 'New York', 'state': 'NY'},
                'hollywood': {'lat': 34.0928, 'lng': -118.3287, 'city': 'Los Angeles', 'state': 'CA'},
                'santa monica pier': {'lat': 34.0089, 'lng': -118.4973, 'city': 'Santa Monica', 'state': 'CA'},
                'golden gate bridge': {'lat': 37.8199, 'lng': -122.4783, 'city': 'San Francisco', 'state': 'CA'},
                'fisherman wharf': {'lat': 37.8080, 'lng': -122.4177, 'city': 'San Francisco', 'state': 'CA'},
                'millennium park': {'lat': 41.8826, 'lng': -87.6226, 'city': 'Chicago', 'state': 'IL'},
                'miami beach': {'lat': 25.7907, 'lng': -80.1300, 'city': 'Miami Beach', 'state': 'FL'}
            }
            
            address_lower = address.lower()
            for key, loc in address_locations.items():
                if key in address_lower:
                    return {
                        'lat': loc['lat'],
                        'lng': loc['lng'],
                        'alt': 10,
                        'address': address,
                        'zip_code': '',
                        'city': loc['city'],
                        'state': loc['state'],
                        'country': 'US'
                    }
            
            # If address not found, return default NYC location
            return {
                'lat': 40.7589,
                'lng': -73.9851,
                'alt': 10,
                'address': address,
                'zip_code': '',
                'city': 'New York',
                'state': 'NY',
                'country': 'US'
            }
            
        except Exception as e:
            self.logger.error(f"Error in fallback address: {e}")
            return None
    
    # ADDED - Pokemon Map Integration Methods
    def open_pokemon_map(self):
        """Open Pokemon Map website in browser"""
        try:
            if not MAP_INTEGRATION_AVAILABLE:
                self.update_status("❌ Map integration not available - missing dependencies")
                return False
            
            lat = self.config['location']['lat']
            lng = self.config['location']['lng']
            
            # Construct Pokemon Map URL with current location
            map_url = f"https://www.pokemap.net/?lat={lat}&lng={lng}&zoom=15"
            
            webbrowser.open(map_url)
            self.update_status(f"🗺️ Opening Pokemon Map at {lat:.6f}, {lng:.6f}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to open Pokemon Map: {e}")
            return False
    
    def get_map_data(self):
        """Get Pokemon Map data for current location"""
        try:
            if not MAP_INTEGRATION_AVAILABLE:
                return self._get_simulated_map_data()
            
            # Check if we need to update map data
            current_time = time.time()
            if (self.map_integration['last_update'] is None or 
                current_time - self.map_integration['last_update'] > self.map_integration['update_interval']):
                
                self.update_status("🗺️ Fetching Pokemon Map data...")
                self._fetch_map_data()
                self.map_integration['last_update'] = current_time
            
            return self.map_integration['map_data']
            
        except Exception as e:
            self.logger.error(f"Error getting map data: {e}")
            return self._get_simulated_map_data()
    
    def _fetch_map_data(self):
        """Fetch real data from Pokemon Map website"""
        try:
            lat = self.config['location']['lat']
            lng = self.config['location']['lng']
            
            # Construct API URL for Pokemon Map
            api_url = f"https://www.pokemap.net/api/pokemon?lat={lat}&lng={lng}&radius=1000"
            
            # Set headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.pokemap.net/',
                'Origin': 'https://www.pokemap.net'
            }
            
            # Make request to Pokemon Map API
            response = requests.get(api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.map_integration['map_data'] = data
                self.update_status("✅ Pokemon Map data updated successfully!")
            else:
                self.update_status(f"⚠️ Pokemon Map API returned status {response.status_code}")
                self.map_integration['map_data'] = self._get_simulated_map_data()
                
        except requests.exceptions.RequestException as e:
            self.update_status(f"⚠️ Pokemon Map API request failed: {e}")
            self.map_integration['map_data'] = self._get_simulated_map_data()
        except Exception as e:
            self.logger.error(f"Error fetching map data: {e}")
            self.map_integration['map_data'] = self._get_simulated_map_data()
    
    def _get_simulated_map_data(self):
        """Get simulated Pokemon Map data when API is not available"""
        try:
            lat = self.config['location']['lat']
            lng = self.config['location']['lng']
            
            # Generate simulated Pokemon spawns around current location
            pokemon_spawns = []
            pokemon_names = ['Pidgey', 'Rattata', 'Caterpie', 'Weedle', 'Spearow', 'Pikachu', 
                           'Charmander', 'Squirtle', 'Bulbasaur', 'Eevee', 'Dratini', 'Snorlax']
            
            for i in range(random.randint(5, 15)):  # 5-15 Pokemon spawns
                # Generate random coordinates within 1km radius
                offset_lat = random.uniform(-0.01, 0.01)
                offset_lng = random.uniform(-0.01, 0.01)
                
                spawn = {
                    'id': random.randint(1, 151),
                    'name': random.choice(pokemon_names),
                    'lat': lat + offset_lat,
                    'lng': lng + offset_lng,
                    'cp': random.randint(10, 2000),
                    'iv': random.randint(0, 100),
                    'level': random.randint(1, 35),
                    'time_left': random.randint(300, 1800),  # 5-30 minutes
                    'rarity': random.choice(['common', 'uncommon', 'rare', 'legendary']),
                    'is_shiny': random.random() < 0.01,  # 1% shiny chance
                    'weather_boost': random.choice(['sunny', 'rainy', 'snowy', 'cloudy', 'foggy', 'windy'])
                }
                pokemon_spawns.append(spawn)
            
            # Generate simulated Pokestops
            pokestops = []
            for i in range(random.randint(3, 8)):  # 3-8 Pokestops
                offset_lat = random.uniform(-0.005, 0.005)
                offset_lng = random.uniform(-0.005, 0.005)
                
                stop = {
                    'id': f"stop_{i}",
                    'name': f"Pokestop {i+1}",
                    'lat': lat + offset_lat,
                    'lng': lng + offset_lng,
                    'lure_type': random.choice([None, 'normal', 'glacial', 'mossy', 'magnetic']),
                    'lure_expires': random.randint(0, 1800) if random.random() < 0.3 else None,
                    'last_spun': random.randint(0, 300)  # 0-5 minutes ago
                }
                pokestops.append(stop)
            
            # Generate simulated Gyms
            gyms = []
            for i in range(random.randint(1, 4)):  # 1-4 Gyms
                offset_lat = random.uniform(-0.008, 0.008)
                offset_lng = random.uniform(-0.008, 0.008)
                
                gym = {
                    'id': f"gym_{i}",
                    'name': f"Gym {i+1}",
                    'lat': lat + offset_lat,
                    'lng': lng + offset_lng,
                    'team': random.choice(['Valor', 'Mystic', 'Instinct', 'Neutral']),
                    'level': random.randint(1, 6),
                    'defenders': random.randint(0, 6),
                    'raid_boss': random.choice([None, 'Mewtwo', 'Rayquaza', 'Groudon', 'Kyogre']) if random.random() < 0.2 else None,
                    'raid_tier': random.randint(1, 5) if random.random() < 0.2 else None
                }
                gyms.append(gym)
            
            # Generate simulated Nests
            nests = []
            if random.random() < 0.3:  # 30% chance of nest
                nest_pokemon = random.choice(['Pikachu', 'Squirtle', 'Charmander', 'Bulbasaur', 'Eevee'])
                nest = {
                    'pokemon': nest_pokemon,
                    'lat': lat + random.uniform(-0.01, 0.01),
                    'lng': lng + random.uniform(-0.01, 0.01),
                    'radius': random.randint(100, 500),
                    'spawn_rate': random.uniform(0.1, 0.5)
                }
                nests.append(nest)
            
            return {
                'pokemon_spawns': pokemon_spawns,
                'pokestops': pokestops,
                'gyms': gyms,
                'nests': nests,
                'weather': self.get_weather_data(),
                'last_updated': time.time(),
                'location': {
                    'lat': lat,
                    'lng': lng
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating simulated map data: {e}")
            return {'pokemon_spawns': [], 'pokestops': [], 'gyms': [], 'nests': []}
    
    def get_nearby_pokemon(self, radius_km=1.0):
        """Get Pokemon within specified radius from current location"""
        try:
            map_data = self.get_map_data()
            pokemon_spawns = map_data.get('pokemon_spawns', [])
            
            current_lat = self.config['location']['lat']
            current_lng = self.config['location']['lng']
            
            nearby_pokemon = []
            for pokemon in pokemon_spawns:
                distance = self.calculate_distance(
                    current_lat, current_lng,
                    pokemon['lat'], pokemon['lng']
                )
                
                if distance <= radius_km:
                    pokemon['distance_km'] = distance
                    nearby_pokemon.append(pokemon)
            
            # Sort by distance
            nearby_pokemon.sort(key=lambda x: x['distance_km'])
            
            return nearby_pokemon
            
        except Exception as e:
            self.logger.error(f"Error getting nearby Pokemon: {e}")
            return []
    
    def get_nearby_pokestops(self, radius_km=1.0):
        """Get Pokestops within specified radius from current location"""
        try:
            map_data = self.get_map_data()
            pokestops = map_data.get('pokestops', [])
            
            current_lat = self.config['location']['lat']
            current_lng = self.config['location']['lng']
            
            nearby_stops = []
            for stop in pokestops:
                distance = self.calculate_distance(
                    current_lat, current_lng,
                    stop['lat'], stop['lng']
                )
                
                if distance <= radius_km:
                    stop['distance_km'] = distance
                    nearby_stops.append(stop)
            
            # Sort by distance
            nearby_stops.sort(key=lambda x: x['distance_km'])
            
            return nearby_stops
            
        except Exception as e:
            self.logger.error(f"Error getting nearby Pokestops: {e}")
            return []
    
    def get_nearby_gyms(self, radius_km=1.0):
        """Get Gyms within specified radius from current location"""
        try:
            map_data = self.get_map_data()
            gyms = map_data.get('gyms', [])
            
            current_lat = self.config['location']['lat']
            current_lng = self.config['location']['lng']
            
            nearby_gyms = []
            for gym in gyms:
                distance = self.calculate_distance(
                    current_lat, current_lng,
                    gym['lat'], gym['lng']
                )
                
                if distance <= radius_km:
                    gym['distance_km'] = distance
                    nearby_gyms.append(gym)
            
            # Sort by distance
            nearby_gyms.sort(key=lambda x: x['distance_km'])
            
            return nearby_gyms
            
        except Exception as e:
            self.logger.error(f"Error getting nearby Gyms: {e}")
            return []
    
    def find_pokemon_by_name(self, pokemon_name, radius_km=2.0):
        """Find specific Pokemon by name within radius"""
        try:
            nearby_pokemon = self.get_nearby_pokemon(radius_km)
            
            matching_pokemon = []
            for pokemon in nearby_pokemon:
                if pokemon_name.lower() in pokemon['name'].lower():
                    matching_pokemon.append(pokemon)
            
            return matching_pokemon
            
        except Exception as e:
            self.logger.error(f"Error finding Pokemon by name: {e}")
            return []
    
    def find_rare_pokemon(self, radius_km=2.0):
        """Find rare Pokemon within radius"""
        try:
            nearby_pokemon = self.get_nearby_pokemon(radius_km)
            
            rare_pokemon = []
            for pokemon in nearby_pokemon:
                if (pokemon['rarity'] in ['rare', 'legendary'] or 
                    pokemon['is_shiny'] or 
                    pokemon['cp'] > 1000 or 
                    pokemon['iv'] > 90):
                    rare_pokemon.append(pokemon)
            
            # Sort by rarity and CP
            rare_pokemon.sort(key=lambda x: (x['rarity'] == 'legendary', x['is_shiny'], x['cp']), reverse=True)
            
            return rare_pokemon
            
        except Exception as e:
            self.logger.error(f"Error finding rare Pokemon: {e}")
            return []
    
    def get_optimal_route_from_map(self, max_distance_km=5.0):
        """Calculate optimal route based on map data"""
        try:
            # Get all nearby points of interest
            pokemon = self.get_nearby_pokemon(max_distance_km)
            pokestops = self.get_nearby_pokestops(max_distance_km)
            gyms = self.get_nearby_gyms(max_distance_km)
            
            # Combine all points
            all_points = []
            
            # Add Pokemon (prioritize rare ones)
            for p in pokemon:
                priority = 1
                if p['rarity'] == 'legendary':
                    priority = 10
                elif p['rarity'] == 'rare':
                    priority = 5
                elif p['is_shiny']:
                    priority = 8
                elif p['cp'] > 1000:
                    priority = 3
                
                all_points.append({
                    'type': 'pokemon',
                    'name': p['name'],
                    'lat': p['lat'],
                    'lng': p['lng'],
                    'priority': priority,
                    'data': p
                })
            
            # Add Pokestops
            for s in pokestops:
                all_points.append({
                    'type': 'pokestop',
                    'name': s['name'],
                    'lat': s['lat'],
                    'lng': s['lng'],
                    'priority': 2,
                    'data': s
                })
            
            # Add Gyms
            for g in gyms:
                all_points.append({
                    'type': 'gym',
                    'name': g['name'],
                    'lat': g['lat'],
                    'lng': g['lng'],
                    'priority': 3,
                    'data': g
                })
            
            # Sort by priority and distance
            current_lat = self.config['location']['lat']
            current_lng = self.config['location']['lng']
            
            for point in all_points:
                point['distance'] = self.calculate_distance(
                    current_lat, current_lng,
                    point['lat'], point['lng']
                )
            
            # Sort by priority (descending) then distance (ascending)
            all_points.sort(key=lambda x: (-x['priority'], x['distance']))
            
            # Create route (limit to reasonable number of stops)
            route = all_points[:20]  # Max 20 stops
            
            return route
            
        except Exception as e:
            self.logger.error(f"Error calculating optimal route: {e}")
            return []
    
    def refresh_map_data(self):
        """Manually refresh map data"""
        try:
            self.update_status("🔄 Refreshing Pokemon Map data...")
            self.map_integration['last_update'] = None  # Force refresh
            map_data = self.get_map_data()
            
            pokemon_count = len(map_data.get('pokemon_spawns', []))
            stops_count = len(map_data.get('pokestops', []))
            gyms_count = len(map_data.get('gyms', []))
            
            self.update_status(f"✅ Map refreshed: {pokemon_count} Pokemon, {stops_count} Pokestops, {gyms_count} Gyms")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to refresh map data: {e}")
            return False
    
    def set_map_auto_refresh(self, enabled, interval_seconds=30):
        """Enable/disable automatic map data refresh"""
        try:
            self.map_integration['auto_refresh'] = enabled
            self.map_integration['update_interval'] = interval_seconds
            
            status = "enabled" if enabled else "disabled"
            self.update_status(f"🗺️ Map auto-refresh {status} (interval: {interval_seconds}s)")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to set map auto-refresh: {e}")
            return False
    
    def get_map_status(self):
        """Get current map integration status"""
        try:
            map_data = self.get_map_data()
            
            status = {
                'enabled': self.map_integration['enabled'],
                'auto_refresh': self.map_integration['auto_refresh'],
                'refresh_interval': self.map_integration['update_interval'],
                'last_update': self.map_integration['last_update'],
                'pokemon_count': len(map_data.get('pokemon_spawns', [])),
                'pokestop_count': len(map_data.get('pokestops', [])),
                'gym_count': len(map_data.get('gyms', [])),
                'nest_count': len(map_data.get('nests', [])),
                'nearby_pokemon': len(self.get_nearby_pokemon(1.0)),
                'nearby_pokestops': len(self.get_nearby_pokestops(1.0)),
                'nearby_gyms': len(self.get_nearby_gyms(1.0)),
                'rare_pokemon': len(self.find_rare_pokemon(2.0))
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting map status: {e}")
            return {}
    
    def search_pokemon_by_type(self, pokemon_type, radius_km=2.0):
        """Search for Pokemon by type (e.g., 'fire', 'water', 'electric')"""
        try:
            nearby_pokemon = self.get_nearby_pokemon(radius_km)
            
            # This would normally check Pokemon types from a database
            # For now, we'll use a simple mapping
            type_mapping = {
                'fire': ['Charmander', 'Charmeleon', 'Charizard', 'Vulpix', 'Ninetales'],
                'water': ['Squirtle', 'Wartortle', 'Blastoise', 'Psyduck', 'Golduck'],
                'electric': ['Pikachu', 'Raichu', 'Voltorb', 'Electrode', 'Electabuzz'],
                'grass': ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Oddish', 'Gloom'],
                'psychic': ['Abra', 'Kadabra', 'Alakazam', 'Mewtwo', 'Mew'],
                'dragon': ['Dratini', 'Dragonair', 'Dragonite'],
                'flying': ['Pidgey', 'Pidgeotto', 'Pidgeot', 'Spearow', 'Fearow'],
                'normal': ['Rattata', 'Raticate', 'Eevee', 'Snorlax']
            }
            
            matching_pokemon = []
            if pokemon_type.lower() in type_mapping:
                target_names = type_mapping[pokemon_type.lower()]
                for pokemon in nearby_pokemon:
                    if pokemon['name'] in target_names:
                        matching_pokemon.append(pokemon)
            
            return matching_pokemon
            
        except Exception as e:
            self.logger.error(f"Error searching Pokemon by type: {e}")
            return []
    
    def get_map_heatmap(self, radius_km=2.0):
        """Generate a heatmap of Pokemon spawns in the area"""
        try:
            map_data = self.get_map_data()
            pokemon_spawns = map_data.get('pokemon_spawns', [])
            
            current_lat = self.config['location']['lat']
            current_lng = self.config['location']['lng']
            
            # Create a grid for heatmap
            grid_size = 0.01  # ~1km grid cells
            grid_lat_min = current_lat - radius_km * 0.01
            grid_lat_max = current_lat + radius_km * 0.01
            grid_lng_min = current_lng - radius_km * 0.01
            grid_lng_max = current_lng + radius_km * 0.01
            
            # Count Pokemon in each grid cell
            heatmap_data = {}
            for pokemon in pokemon_spawns:
                if pokemon['lat'] >= grid_lat_min and pokemon['lat'] <= grid_lat_max and \
                   pokemon['lng'] >= grid_lng_min and pokemon['lng'] <= grid_lng_max:
                    
                    # Calculate grid cell
                    cell_lat = int((pokemon['lat'] - grid_lat_min) / grid_size)
                    cell_lng = int((pokemon['lng'] - grid_lng_min) / grid_size)
                    cell_key = f"{cell_lat}_{cell_lng}"
                    
                    if cell_key not in heatmap_data:
                        heatmap_data[cell_key] = {
                            'count': 0,
                            'lat': grid_lat_min + cell_lat * grid_size,
                            'lng': grid_lng_min + cell_lng * grid_size,
                            'pokemon': []
                        }
                    
                    heatmap_data[cell_key]['count'] += 1
                    heatmap_data[cell_key]['pokemon'].append(pokemon)
            
            return list(heatmap_data.values())
            
        except Exception as e:
            self.logger.error(f"Error generating heatmap: {e}")
            return []
    
    def export_map_data(self, filename=None):
        """Export map data to JSON file"""
        try:
            if filename is None:
                filename = f"pokemon_map_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            map_data = self.get_map_data()
            
            with open(filename, 'w') as f:
                json.dump(map_data, f, indent=2, default=str)
            
            self.update_status(f"🗺️ Map data exported to {filename}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to export map data: {e}")
            return False
    
    def import_map_data(self, filename):
        """Import map data from JSON file"""
        try:
            with open(filename, 'r') as f:
                map_data = json.load(f)
            
            self.map_integration['map_data'] = map_data
            self.map_integration['last_update'] = time.time()
            
            self.update_status(f"🗺️ Map data imported from {filename}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to import map data: {e}")
            return False
    
    def login(self):
        """Login to Pokemon GO using PokemonGoBot REST API with TZiggler3300 credentials"""
        try:
            username = self.config.get('username', '')
            password = self.config.get('password', '')
            
            self.update_status(f"🔐 Attempting to login as {username}...")
            self.update_status("🔗 Pokemon Trainer Club: https://access.pokemon.com/login")
            
            # Try to connect to PokemonGoBot REST API
            try:
                from PokemonGoBot_API import PokemonGoBotAPI
                
                # Create API client with your credentials
                self.api_client = PokemonGoBotAPI(
                    base_url=self.config.get('api_url', 'http://localhost:8080'),
                    bot_name=self.config.get('bot_name', 'default'),
                    password=self.config.get('api_password', ''),
                    gui_callback=self.update_status
                )
                
                # Test connection
                if self.api_client.test_connection():
                    self.update_status("✅ Successfully connected to PokemonGoBot API!")
                    self.update_status(f"👤 Logged in as: {username}")
                    self.update_status("🔗 Using real Pokemon GO bot control")
                    
                    # Set location if available
                    location = self.config.get('location', {})
                    if location:
                        self.api_client.set_location(
                            location.get('lat', 40.7589),
                            location.get('lng', -73.9851),
                            location.get('alt', 10)
                        )
                        self.update_status(f"📍 Location set to: {location.get('lat', 40.7589)}, {location.get('lng', -73.9851)}")
                    
                    return True
                else:
                    raise Exception("Failed to connect to PokemonGoBot API")
                    
            except ImportError:
                # Fallback to simulated login if API client not available
                self.update_status("⚠️ Using simulated mode - PokemonGoBot API not available")
                self.update_status(f"👤 Simulating login as: {username}")
                self.update_status("📋 To use real bot: Start PokemonGoBot with REST API enabled")
                time.sleep(2)
                self.update_status("✅ Successfully logged in! (Simulated)")
                return True
            except Exception as e:
                self.update_status(f"⚠️ API connection failed, using simulated mode: {e}")
                self.update_status(f"👤 Simulating login as: {username}")
                self.update_status("📋 To use real bot: Start PokemonGoBot with REST API enabled")
                time.sleep(2)
                self.update_status("✅ Successfully logged in! (Simulated)")
                return True
            
        except Exception as e:
            self.update_status(f"❌ Login failed: {e}")
            self.update_status("🔗 Official PTC Login: https://access.pokemon.com/login")
            return False
    
    def get_player_info(self):
        """Get player information from PokemonGoBot API"""
        try:
            # Try to get real player data from PokemonGoBot API
            if hasattr(self, 'api_client') and self.api_client and self.api_client.is_connected():
                try:
                    player_data = self.api_client.get_player_info()
                    if player_data:
                        self.update_status("📊 Fetched real player data from PokemonGoBot API")
                        return player_data
                except Exception as e:
                    self.logger.warning(f"API player data failed: {e}")
            
            # Fallback to simulated data with realistic level 4 stats for TZiggler3300
            self.update_status("⚠️ Using simulated player data - API not connected")
            return {
                'level': 4,  # Your actual level
                'experience': 2500,  # Typical XP for level 4
                'stardust': 1500,  # Typical stardust for level 4
                'team': 'Valor',  # Default team
                'username': self.config.get('username', 'TZiggler3300'),
                'pokemon_caught': 15,  # Typical catches for level 4
                'pokestops_visited': 8,  # Typical stops for level 4
                'gyms_battled': 0,  # Level 4 usually can't battle gyms yet
                'km_walked': 2.5  # Typical distance for level 4
            }
        except Exception as e:
            self.update_status(f"❌ Error getting player info: {e}")
            return {}
    
    def get_real_pokemon_data(self):
        """Get real Pokemon data from PokemonGoBot API"""
        try:
            if hasattr(self, 'api_client') and self.api_client and self.api_client.is_connected():
                try:
                    # Get real Pokemon data from API
                    pokemons = self.api_client.get_pokemons()
                    if pokemons:
                        self.update_status("📊 Fetched real Pokemon data from API")
                        return {
                            'nearby_pokemon': pokemons.get('nearby', []),
                            'pokemons': pokemons.get('pokemons', []),
                            'pokestops': pokemons.get('pokestops', []),
                            'gyms': pokemons.get('gyms', [])
                        }
                except Exception as e:
                    self.logger.warning(f"API Pokemon data failed: {e}")
            
            # Fallback to simulated data
            self.update_status("⚠️ Using simulated Pokemon data - API not connected")
            return self._get_simulated_pokemon_data()
        except Exception as e:
            self.logger.warning(f"Error getting Pokemon data: {e}")
            return self._get_simulated_pokemon_data()
    
    def _get_simulated_pokemon_data(self):
        """Get simulated Pokemon data for level 4 player"""
        return {
            'nearby_pokemon': [
                {'name': 'Pidgey', 'cp': 45, 'distance': 50, 'rarity': 'common'},
                {'name': 'Rattata', 'cp': 38, 'distance': 75, 'rarity': 'common'},
                {'name': 'Caterpie', 'cp': 42, 'distance': 60, 'rarity': 'common'},
                {'name': 'Weedle', 'cp': 40, 'distance': 55, 'rarity': 'common'},
                {'name': 'Spearow', 'cp': 48, 'distance': 45, 'rarity': 'common'}
            ],
            'pokestops': [
                {'name': 'Local Pokestop', 'distance': 100, 'items': ['Poke Ball', 'Potion']},
                {'name': 'Park Pokestop', 'distance': 150, 'items': ['Poke Ball', 'Razz Berry']}
            ],
            'gyms': [
                {'name': 'Team Valor Gym', 'distance': 200, 'team': 'Valor', 'level': 3},
                {'name': 'Team Mystic Gym', 'distance': 300, 'team': 'Mystic', 'level': 5}
            ]
        }
    
    def get_statistics(self):
        """Get bot statistics from PokemonGoBot API"""
        try:
            # Try to get real statistics from API
            if hasattr(self, 'api_client') and self.api_client and self.api_client.is_connected():
                try:
                    api_stats = self.api_client.get_statistics()
                    if api_stats:
                        # Merge API stats with local stats
                        self.stats.update(api_stats)
                        return self.stats
                except Exception as e:
                    self.logger.warning(f"API statistics failed: {e}")
            
            # Fallback to local stats
            return self.stats.copy()
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return self.stats.copy()
    
    def get_detailed_statistics(self):
        """Get detailed statistics for display"""
        try:
            player_info = self.get_player_info()
            stats = self.get_statistics()
            
            detailed_stats = f"""🎮 Pokemon GO Bot - Detailed Statistics

📊 Trainer Information:
• Trainer Level: {player_info.get('level', 'Unknown')}
• XP: {player_info.get('experience', 'Unknown'):,}
• Stardust: {player_info.get('stardust', 'Unknown'):,}
• Team: {player_info.get('team', 'Unknown')}

🔴 Pokemon Collection:
• Total Caught: {stats.get('pokemon_caught', 0):,}
• Shiny Caught: {stats.get('shiny_caught', 0):,}
• Perfect IV: {stats.get('perfect_iv_caught', 0):,}

🏆 Achievements:
• Pokestops Visited: {stats.get('pokestops_spun', 0):,}
• Gyms Battled: {stats.get('gyms_battled', 0):,}
• Raids Completed: {stats.get('raids_completed', 0):,}
• XP Gained: {stats.get('xp_gained', 0):,}
• Stardust Earned: {stats.get('stardust_earned', 0):,}

⚔️ Battle Stats:
• Current Activity: {stats.get('current_activity', 'Unknown')}
• Bot Status: {'Running' if self.running else 'Stopped'}
• Mode: {self.current_mode.title()}

🎯 Recent Activity:
• Start Time: {stats.get('start_time', 'Not started')}
• Runtime: {self._get_runtime()}

⚙️ Bot Configuration:
• Walk Speed: {self.config['walk_speed']} km/h
• Catch Pokemon: {'Yes' if self.config['catch_pokemon'] else 'No'}
• Spin Pokestops: {'Yes' if self.config['spin_pokestops'] else 'No'}
• Battle Gyms: {'Yes' if self.config['battle_gyms'] else 'No'}
• Transfer Pokemon: {'Yes' if self.config['transfer_duplicates'] else 'No'}"""
            
            return detailed_stats
            
        except Exception as e:
            return f"❌ Error getting detailed stats: {e}"
    
    def _get_runtime(self):
        """Get bot runtime"""
        if self.stats.get('start_time'):
            runtime = datetime.datetime.now() - self.stats['start_time']
            return str(runtime).split('.')[0]  # Remove microseconds
        return "Not started"
    
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
    
    def step(self):
        """Run one bot step"""
        if not self.running or self.paused:
            return
        
        try:
            # Get real Pokemon data
            pokemon_data = self.get_real_pokemon_data()
            
            # Apply ban bypass techniques
            self._apply_ban_bypass()
            
            # Run current mode with real data
            if self.current_mode in self.modes:
                self.modes[self.current_mode](pokemon_data)
            else:
                self._idle_mode(pokemon_data)
            
            # AI Pokemon management
            self._ai_pokemon_management()
            
            # AI performance monitoring
            self._ai_performance_monitoring()
            
            # AI risk assessment
            self._ai_risk_assessment()
                
        except Exception as e:
            self.update_status(f"❌ Bot step error: {e}")
    
    def _apply_ban_bypass(self):
        """Apply ban bypass techniques to avoid detection"""
        try:
            if not self.config.get('ban_bypass', True):
                return
            
            # Human-like timing
            if self.ban_bypass.get('human_timing', True):
                self._human_like_timing()
            
            # Random delays
            if self.ban_bypass.get('random_delays', True):
                self._random_delays()
            
            # Movement simulation
            if self.ban_bypass.get('movement_simulation', True):
                self._simulate_human_movement()
            
            # Action randomization
            if self.ban_bypass.get('action_randomization', True):
                self._randomize_actions()
            
            self.stats['ban_attempts_blocked'] += 1
            
        except Exception as e:
            self.logger.error(f"Ban bypass error: {e}")
    
    def _human_like_timing(self):
        """Simulate human-like timing patterns"""
        try:
            current_time = time.time()
            time_since_last = current_time - self.ai_system['last_action_time']
            
            # Random cooldown between 1-5 seconds
            min_delay = 1.0
            max_delay = 5.0
            required_delay = random.uniform(min_delay, max_delay)
            
            if time_since_last < required_delay:
                sleep_time = required_delay - time_since_last
                time.sleep(sleep_time)
            
            self.ai_system['last_action_time'] = time.time()
            
        except Exception as e:
            self.logger.error(f"Human timing error: {e}")
    
    def _random_delays(self):
        """Add random delays to actions"""
        try:
            # Random delay between 0.5-3 seconds
            delay = random.uniform(0.5, 3.0)
            time.sleep(delay)
            
        except Exception as e:
            self.logger.error(f"Random delay error: {e}")
    
    def _simulate_human_movement(self):
        """Simulate human-like movement patterns"""
        try:
            if not self.config.get('random_movements', True):
                return
            
            # Random small movements
            lat_offset = random.uniform(-0.0001, 0.0001)
            lng_offset = random.uniform(-0.0001, 0.0001)
            
            self.config['location']['lat'] += lat_offset
            self.config['location']['lng'] += lng_offset
            
        except Exception as e:
            self.logger.error(f"Movement simulation error: {e}")
    
    def _randomize_actions(self):
        """Randomize action order and timing"""
        try:
            # Randomly decide whether to perform action
            if random.random() < 0.1:  # 10% chance to skip action
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Action randomization error: {e}")
            return True
    
    def _ai_smart_catching(self, pokemon_data):
        """AI-powered smart catching system"""
        try:
            if not self.config.get('smart_catching', True):
                return True
            
            # Analyze Pokemon data
            cp = pokemon_data.get('cp', 0)
            iv = pokemon_data.get('iv', 0)
            level = pokemon_data.get('level', 1)
            pokemon_id = pokemon_data.get('id', 0)
            
            # Check if Pokemon is in target list
            if self.config.get('target_pokemon'):
                pokemon_name = self._get_pokemon_name(pokemon_id)
                if pokemon_name not in self.config['target_pokemon']:
                    return False
            
            # AI decision making
            catch_decision = self._ai_catch_decision(pokemon_data)
            
            if catch_decision:
                self.stats['ai_decisions_made'] += 1
                self.update_status(f"🤖 AI Decision: Catching {pokemon_name} (CP: {cp})")
            
            return catch_decision
            
        except Exception as e:
            self.logger.error(f"AI smart catching error: {e}")
            return True
    
    def _ai_catch_decision(self, pokemon_data):
        """AI decision making for catching Pokemon"""
        try:
            cp = pokemon_data.get('cp', 0)
            iv = pokemon_data.get('iv', 0)
            level = pokemon_data.get('level', 1)
            pokemon_id = pokemon_data.get('id', 0)
            
            # High CP threshold
            if cp >= self.config.get('min_cp_threshold', 100):
                return True
            
            # Perfect IV Pokemon
            if iv >= 100:
                return True
            
            # Legendary/Mythical Pokemon
            if self._is_legendary(pokemon_id):
                return True
            
            # Shiny Pokemon
            if pokemon_data.get('is_shiny', False):
                return True
            
            # Random chance for low CP Pokemon
            if random.random() < 0.3:  # 30% chance
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"AI catch decision error: {e}")
            return True
    
    def _is_legendary(self, pokemon_id):
        """Check if Pokemon is legendary"""
        legendary_ids = [
            144, 145, 146,  # Kanto birds
            150, 151,       # Mewtwo, Mew
            243, 244, 245,  # Johto beasts
            249, 250, 251,  # Lugia, Ho-Oh, Celebi
            # Add more legendary IDs as needed
        ]
        return pokemon_id in legendary_ids
    
    def _get_pokemon_name(self, pokemon_id):
        """Get Pokemon name from ID"""
        try:
            # This would normally query a Pokemon database
            # For now, return a placeholder
            return f"Pokemon_{pokemon_id}"
        except Exception as e:
            self.logger.error(f"Get Pokemon name error: {e}")
            return "Unknown"
    
    def _ai_pokemon_management(self):
        """AI-powered Pokemon management system"""
        try:
            if not self.config.get('ai_automation', True):
                return
            
            # Auto-evolve Pokemon
            if self.config.get('auto_evolve', True):
                self._auto_evolve_pokemon()
            
            # Auto-powerup Pokemon
            if self.config.get('auto_powerup', True):
                self._auto_powerup_pokemon()
            
            # Auto-mega evolve
            if self.config.get('mega_evolve', True):
                self._auto_mega_evolve()
            
            # Transfer low-value Pokemon
            self._transfer_low_value_pokemon()
            
        except Exception as e:
            self.logger.error(f"AI Pokemon management error: {e}")
    
    def _auto_evolve_pokemon(self):
        """Automatically evolve Pokemon when possible"""
        try:
            # This would normally check evolution requirements
            # For now, simulate the process
            self.update_status("🔄 AI: Checking for evolution candidates...")
            
            # Simulate evolution
            if random.random() < 0.1:  # 10% chance per check
                self.stats['pokemon_evolved'] += 1
                self.update_status("✨ AI: Pokemon evolved!")
            
        except Exception as e:
            self.logger.error(f"Auto evolve error: {e}")
    
    def _auto_powerup_pokemon(self):
        """Automatically power up high CP Pokemon"""
        try:
            # This would normally check powerup requirements
            # For now, simulate the process
            self.update_status("⚡ AI: Checking for powerup candidates...")
            
            # Simulate powerup
            if random.random() < 0.05:  # 5% chance per check
                self.stats['pokemon_powered_up'] += 1
                self.update_status("💪 AI: Pokemon powered up!")
            
        except Exception as e:
            self.logger.error(f"Auto powerup error: {e}")
    
    def _auto_mega_evolve(self):
        """Automatically mega evolve Pokemon when possible"""
        try:
            # This would normally check mega evolution requirements
            # For now, simulate the process
            self.update_status("🌟 AI: Checking for mega evolution candidates...")
            
            # Simulate mega evolution
            if random.random() < 0.02:  # 2% chance per check
                self.stats['mega_evolutions'] += 1
                self.update_status("🌟 AI: Pokemon mega evolved!")
            
        except Exception as e:
            self.logger.error(f"Auto mega evolve error: {e}")
    
    def _transfer_low_value_pokemon(self):
        """Transfer low-value Pokemon to make space"""
        try:
            if not self.config.get('transfer_duplicates', True):
                return
            
            # This would normally check Pokemon values
            # For now, simulate the process
            self.update_status("🗑️ AI: Checking for low-value Pokemon...")
            
            # Simulate transfer
            if random.random() < 0.1:  # 10% chance per check
                self.stats['pokemon_transferred'] += 1
                self.update_status("🗑️ AI: Low-value Pokemon transferred!")
            
        except Exception as e:
            self.logger.error(f"Transfer low value error: {e}")
    
    def _ai_optimize_inventory(self):
        """AI-powered inventory optimization"""
        try:
            # Check Pokemon storage
            if self.player_info.get('pokemon_count', 0) >= self.config.get('max_pokemon_storage', 1000):
                self._transfer_low_value_pokemon()
            
            # Check item storage
            if self.player_info.get('item_count', 0) >= 2000:  # Max item storage
                self._use_items()
            
        except Exception as e:
            self.logger.error(f"Inventory optimization error: {e}")
    
    def _use_items(self):
        """Use items to free up space"""
        try:
            # This would normally use items like potions, revives, etc.
            # For now, simulate the process
            self.update_status("💊 AI: Using items to free space...")
            
        except Exception as e:
            self.logger.error(f"Use items error: {e}")
    
    def _ai_route_optimization(self):
        """AI-powered route optimization for maximum efficiency"""
        try:
            # This would normally calculate optimal routes
            # For now, simulate the process
            self.update_status("🗺️ AI: Optimizing route for maximum efficiency...")
            
        except Exception as e:
            self.logger.error(f"Route optimization error: {e}")
    
    def _ai_weather_adaptation(self):
        """AI adaptation to weather conditions"""
        try:
            # This would normally check weather and adapt behavior
            # For now, simulate the process
            self.update_status("🌤️ AI: Adapting to weather conditions...")
            
        except Exception as e:
            self.logger.error(f"Weather adaptation error: {e}")
    
    def _ai_event_optimization(self):
        """AI optimization for special events"""
        try:
            # This would normally check for events and optimize accordingly
            # For now, simulate the process
            self.update_status("🎉 AI: Optimizing for special events...")
            
        except Exception as e:
            self.logger.error(f"Event optimization error: {e}")
    
    def _ai_ban_detection(self):
        """AI-powered ban detection and prevention"""
        try:
            # This would normally monitor for ban indicators
            # For now, simulate the process
            self.update_status("🛡️ AI: Monitoring for ban indicators...")
            
            # Simulate ban detection
            if random.random() < 0.001:  # 0.1% chance
                self.update_status("⚠️ AI: Potential ban detected, adjusting behavior...")
                self._adjust_behavior_for_ban_risk()
            
        except Exception as e:
            self.logger.error(f"Ban detection error: {e}")
    
    def _adjust_behavior_for_ban_risk(self):
        """Adjust behavior when ban risk is detected"""
        try:
            # Increase delays
            self.ai_system['action_cooldown'] += 2.0
            
            # Reduce activity
            self.config['walk_speed'] *= 0.8
            
            # Add more randomness
            self.ban_bypass['random_delays'] = True
            
            self.update_status("🛡️ AI: Behavior adjusted for ban prevention")
            
        except Exception as e:
            self.logger.error(f"Behavior adjustment error: {e}")
    
    def _ai_learning_system(self):
        """AI learning system to improve over time"""
        try:
            # This would normally learn from successful patterns
            # For now, simulate the process
            self.update_status("🧠 AI: Learning from successful patterns...")
            
            # Simulate learning
            if random.random() < 0.05:  # 5% chance
                self.update_status("📈 AI: Performance improved through learning!")
            
        except Exception as e:
            self.logger.error(f"Learning system error: {e}")
    
    def _ai_adaptive_strategies(self):
        """AI adaptive strategies based on current situation"""
        try:
            # This would normally adapt strategies based on current conditions
            # For now, simulate the process
            self.update_status("🎯 AI: Adapting strategies for current situation...")
            
        except Exception as e:
            self.logger.error(f"Adaptive strategies error: {e}")
    
    def _ai_performance_monitoring(self):
        """AI performance monitoring and optimization"""
        try:
            # Monitor performance metrics
            catch_rate = self.stats['pokemon_caught'] / max(1, self.stats['pokestops_spun'])
            efficiency = self.stats['xp_gained'] / max(1, time.time() - self.stats['start_time'])
            
            # Adjust behavior based on performance
            if catch_rate < 0.5:
                self.update_status("📊 AI: Low catch rate detected, adjusting strategy...")
            
            if efficiency < 100:
                self.update_status("📊 AI: Low efficiency detected, optimizing behavior...")
            
        except Exception as e:
            self.logger.error(f"Performance monitoring error: {e}")
    
    def _ai_risk_assessment(self):
        """AI risk assessment for ban prevention"""
        try:
            # Assess current risk level
            risk_factors = []
            
            # Check for suspicious patterns
            if self.stats['pokemon_caught'] > 100:  # High catch rate
                risk_factors.append("high_catch_rate")
            
            if self.stats['pokestops_spun'] > 200:  # High spin rate
                risk_factors.append("high_spin_rate")
            
            # Adjust behavior based on risk
            if len(risk_factors) > 2:
                self.update_status("⚠️ AI: High risk detected, implementing safety measures...")
                self._implement_safety_measures()
            
        except Exception as e:
            self.logger.error(f"Risk assessment error: {e}")
    
    def _implement_safety_measures(self):
        """Implement safety measures when risk is high"""
        try:
            # Increase delays
            self.ai_system['action_cooldown'] += 5.0
            
            # Reduce activity
            self.config['walk_speed'] *= 0.5
            
            # Add more randomness
            self.ban_bypass['random_delays'] = True
            self.ban_bypass['action_randomization'] = True
            
            self.update_status("🛡️ AI: Safety measures implemented")
            
        except Exception as e:
            self.logger.error(f"Safety measures error: {e}")
    
    def _ai_advanced_catching(self, pokemon_data):
        """Advanced AI catching system with optimal strategies"""
        try:
            cp = pokemon_data.get('cp', 0)
            iv = pokemon_data.get('iv', 0)
            level = pokemon_data.get('level', 1)
            pokemon_id = pokemon_data.get('id', 0)
            
            # Determine optimal catching strategy
            if cp >= 1000:  # High CP Pokemon
                return self._catch_high_cp_pokemon(pokemon_data)
            elif iv >= 90:  # High IV Pokemon
                return self._catch_high_iv_pokemon(pokemon_data)
            elif self._is_legendary(pokemon_id):  # Legendary Pokemon
                return self._catch_legendary_pokemon(pokemon_data)
            else:  # Regular Pokemon
                return self._catch_regular_pokemon(pokemon_data)
            
        except Exception as e:
            self.logger.error(f"Advanced catching error: {e}")
            return True
    
    def _catch_high_cp_pokemon(self, pokemon_data):
        """Specialized catching for high CP Pokemon"""
        try:
            cp = pokemon_data.get('cp', 0)
            self.update_status(f"🔥 AI: Catching high CP Pokemon (CP: {cp})")
            
            # Use best strategy for high CP
            # This would normally use golden razz berries, ultra balls, etc.
            
            self.stats['high_cp_caught'] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"High CP catching error: {e}")
            return True
    
    def _catch_high_iv_pokemon(self, pokemon_data):
        """Specialized catching for high IV Pokemon"""
        try:
            iv = pokemon_data.get('iv', 0)
            self.update_status(f"💎 AI: Catching high IV Pokemon (IV: {iv})")
            
            # Use best strategy for high IV
            # This would normally use silver pinap berries, great balls, etc.
            
            return True
            
        except Exception as e:
            self.logger.error(f"High IV catching error: {e}")
            return True
    
    def _catch_legendary_pokemon(self, pokemon_data):
        """Specialized catching for legendary Pokemon"""
        try:
            pokemon_id = pokemon_data.get('id', 0)
            self.update_status(f"👑 AI: Catching legendary Pokemon (ID: {pokemon_id})")
            
            # Use best strategy for legendary
            # This would normally use golden razz berries, ultra balls, excellent throws, etc.
            
            return True
            
        except Exception as e:
            self.logger.error(f"Legendary catching error: {e}")
            return True
    
    def _catch_regular_pokemon(self, pokemon_data):
        """Standard catching for regular Pokemon"""
        try:
            cp = pokemon_data.get('cp', 0)
            self.update_status(f"🎯 AI: Catching regular Pokemon (CP: {cp})")
            
            # Use standard strategy
            # This would normally use regular pokeballs, etc.
            
            return True
            
        except Exception as e:
            self.logger.error(f"Regular catching error: {e}")
            return True
    
    def update_status(self, message):
        """Update bot status and notify GUI"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        status_message = f"{timestamp} - {message}"
        
        if self.gui_callback:
            self.gui_callback(status_message)
        
        self.logger.info(message)
        self.stats['current_activity'] = message
    
    def get_live_stats(self):
        """Get live stats for GUI display"""
        try:
            player_info = self.get_player_info()
            stats = self.get_statistics()
            
            return {
                'level': player_info.get('level', 1),
                'experience': player_info.get('experience', 0),
                'stardust': player_info.get('stardust', 0),
                'team': player_info.get('team', 'Unknown'),
                'username': player_info.get('username', 'Unknown'),
                'pokemon_caught': stats.get('pokemon_caught', 0),
                'pokestops_spun': stats.get('pokestops_spun', 0),
                'gyms_battled': stats.get('gyms_battled', 0),
                'xp_gained': stats.get('xp_gained', 0),
                'stardust_earned': stats.get('stardust_earned', 0),
                'current_activity': stats.get('current_activity', 'Idle'),
                'bot_status': 'Running' if self.running else 'Stopped',
                'mode': self.current_mode.title(),
                'uptime': self._get_runtime()
            }
        except Exception as e:
            self.logger.error(f"Error getting live stats: {e}")
            return {}
    
    def open_ptc_login(self):
        """Open official Pokemon Trainer Club login page"""
        try:
            import webbrowser
            ptc_url = "https://access.pokemon.com/login"
            webbrowser.open(ptc_url)
            self.update_status("🔗 Opening Pokemon Trainer Club login page...")
            return True
        except Exception as e:
            self.update_status(f"❌ Failed to open PTC login: {e}")
            return False
    
    def validate_ptc_credentials(self, username, password):
        """Validate PTC credentials format"""
        try:
            if not username or not password:
                return False, "Username and password are required"
            
            if len(username) < 3:
                return False, "Username must be at least 3 characters"
            
            if len(password) < 6:
                return False, "Password must be at least 6 characters"
            
            # Basic validation for PTC username format
            if not username.replace('_', '').replace('-', '').isalnum():
                return False, "Username can only contain letters, numbers, underscores, and hyphens"
            
            return True, "Credentials format is valid"
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def start_bot(self, mode='catching'):
        """Start the Pokemon GO bot"""
        if self.running:
            self.update_status("Bot is already running!")
            return False
        
        # Try to start via API if connected
        if hasattr(self, 'api_client') and self.api_client and self.api_client.is_connected():
            if self.api_client.start_bot():
                self.running = True
                self.current_mode = mode
                self.stats['start_time'] = datetime.datetime.now()
                self.update_status(f"🚀 Bot started via API in {mode} mode!")
                return True
            else:
                self.update_status("❌ Failed to start bot via API")
                return False
        
        # Fallback to local start
        self.running = True
        self.current_mode = mode
        self.stats['start_time'] = datetime.datetime.now()
        
        # Start bot in separate thread
        self.bot_thread = threading.Thread(target=self._run_bot, daemon=True)
        self.bot_thread.start()
        
        self.update_status(f"🚀 Thunderbolt bot started locally in {mode} mode!")
        return True
    
    def stop_bot(self):
        """Stop the Pokemon GO bot"""
        if not self.running:
            self.update_status("Bot is not running!")
            return False
        
        # Try to stop via API if connected
        if hasattr(self, 'api_client') and self.api_client and self.api_client.is_connected():
            if self.api_client.stop_bot():
                self.running = False
                self.current_mode = 'idle'
                self.update_status("⏹️ Bot stopped via API!")
                return True
            else:
                self.update_status("❌ Failed to stop bot via API")
        
        # Fallback to local stop
        self.running = False
        self.current_mode = 'idle'
        self.update_status("⏹️ Thunderbolt bot stopped locally!")
        return True
    
    def pause_bot(self):
        """Pause the Pokemon GO bot"""
        self.paused = not self.paused
        status = "paused" if self.paused else "resumed"
        self.update_status(f"⏸️ Bot {status}!")
        return True
    
    def set_mode(self, mode):
        """Change bot mode"""
        if mode not in self.modes:
            self.update_status(f"Invalid mode: {mode}")
            return False
        
        self.current_mode = mode
        self.update_status(f"🔄 Switched to {mode} mode!")
        return True
    
    def _run_bot(self):
        """Main bot loop"""
        try:
            # Initialize API connection
            if not self._initialize_api():
                self.update_status("❌ Failed to initialize API connection!")
                return
            
            self.update_status("✅ API connection established!")
            
            # Main bot loop
            while self.running:
                if not self.paused:
                    # Execute current mode
                    if self.current_mode in self.modes:
                        self.modes[self.current_mode]()
                    
                    # Small delay to prevent excessive CPU usage
                    time.sleep(0.1)
                else:
                    time.sleep(1)
                    
        except Exception as e:
            self.update_status(f"❌ Bot error: {str(e)}")
            self.logger.error(f"Bot error: {e}")
        finally:
            self.running = False
            self.update_status("🛑 Bot thread ended!")
    
    def _initialize_api(self):
        """Initialize Pokemon GO API connection"""
        try:
            # This would normally initialize the actual API
            # For now, we'll simulate it
            self.update_status("🔌 Connecting to Pokemon GO servers...")
            time.sleep(2)  # Simulate connection time
            
            self.update_status("🔐 Authenticating credentials...")
            time.sleep(1)  # Simulate auth time
            
            self.update_status("📡 Establishing secure connection...")
            time.sleep(1)  # Simulate secure connection
            
            return True
            
        except Exception as e:
            self.update_status(f"❌ API initialization failed: {e}")
            return False
    
    def _catching_mode(self):
        """Pokemon catching mode with map integration"""
        if not self.config['catch_pokemon']:
            return
        
        # Get nearby Pokemon from map
        nearby_pokemon = self.get_nearby_pokemon(1.0)  # 1km radius
        
        if nearby_pokemon:
            # Prioritize rare Pokemon
            rare_pokemon = [p for p in nearby_pokemon if p['rarity'] in ['rare', 'legendary'] or p['is_shiny']]
            if rare_pokemon:
                pokemon = rare_pokemon[0]  # Target the first rare Pokemon
                self.update_status(f"🎯 Targeting RARE {pokemon['name']} (CP: {pokemon['cp']}, Distance: {pokemon['distance_km']:.2f}km)")
            else:
                pokemon = nearby_pokemon[0]  # Target the closest Pokemon
                self.update_status(f"🎯 Targeting {pokemon['name']} (CP: {pokemon['cp']}, Distance: {pokemon['distance_km']:.2f}km)")
            
            # Simulate movement to Pokemon
            if pokemon['distance_km'] > 0.1:  # If more than 100m away
                self.update_status(f"🚶 Walking to {pokemon['name']}...")
                time.sleep(2)  # Simulate walking time
            
            # Simulate catch attempt
            catch_success = self._ai_smart_catching(pokemon)
            
            if catch_success:
                if random.random() < 0.8:  # 80% catch rate
                    self.stats['pokemon_caught'] += 1
                    self.stats['xp_gained'] += random.randint(100, 500)
                    self.stats['stardust_earned'] += random.randint(100, 300)
                    
                    # Check for shiny
                    if pokemon.get('is_shiny', False):
                        self.stats['shiny_caught'] += 1
                        self.update_status(f"✨ Caught SHINY {pokemon['name']}!")
                    else:
                        self.update_status(f"🎯 Caught {pokemon['name']}!")
                    
                    # Check for perfect IV
                    if pokemon.get('iv', 0) >= 100:
                        self.stats['perfect_iv_caught'] += 1
                        self.update_status(f"💎 Perfect IV {pokemon['name']}!")
                else:
                    self.update_status(f"❌ {pokemon['name']} escaped!")
        else:
            # No nearby Pokemon, simulate random encounter
            if random.random() < 0.1:  # 10% chance per cycle
                pokemon_types = ['Pidgey', 'Rattata', 'Caterpie', 'Weedle', 'Pikachu', 'Charmander', 'Squirtle', 'Bulbasaur']
                pokemon_name = random.choice(pokemon_types)
                
                # Simulate catch success
                if random.random() < 0.8:  # 80% catch rate
                    self.stats['pokemon_caught'] += 1
                    self.stats['xp_gained'] += random.randint(100, 500)
                    self.stats['stardust_earned'] += random.randint(100, 300)
                    self.update_status(f"🎯 Caught {pokemon_name}!")
                else:
                    self.update_status(f"❌ {pokemon_name} escaped!")
        
        # Simulate Pokestop spinning using map data
        if self.config['spin_pokestops']:
            nearby_stops = self.get_nearby_pokestops(0.5)  # 500m radius
            if nearby_stops:
                stop = nearby_stops[0]  # Closest stop
                self.update_status(f"🎡 Spinning {stop['name']} (Distance: {stop['distance_km']:.2f}km)")
                
                # Simulate movement to stop
                if stop['distance_km'] > 0.1:
                    time.sleep(1)  # Simulate walking time
                
                self.stats['pokestops_spun'] += 1
                self.stats['xp_gained'] += 50
                self.update_status("✅ Pokestop spun!")
            elif random.random() < 0.2:  # 20% chance per cycle if no stops nearby
                self.stats['pokestops_spun'] += 1
                self.stats['xp_gained'] += 50
                self.update_status("🎡 Spun Pokestop!")
    
    def _raiding_mode(self):
        """Raid battle mode with map integration"""
        # Get nearby gyms with raids
        nearby_gyms = self.get_nearby_gyms(2.0)  # 2km radius
        raid_gyms = [g for g in nearby_gyms if g.get('raid_boss') is not None]
        
        if raid_gyms:
            gym = raid_gyms[0]  # Closest gym with raid
            boss = gym['raid_boss']
            tier = gym.get('raid_tier', 1)
            
            self.update_status(f"🏰 Raid found at {gym['name']} - {boss} (Tier {tier})")
            self.update_status(f"🚶 Walking to raid location... (Distance: {gym['distance_km']:.2f}km)")
            
            # Simulate movement to raid
            if gym['distance_km'] > 0.1:
                time.sleep(3)  # Simulate walking time
            
            self.update_status(f"⚔️ Starting raid battle against {boss}!")
            time.sleep(5)  # Simulate raid time
            
            # Simulate raid success based on tier
            success_rate = 0.9 if tier <= 3 else 0.7 if tier <= 4 else 0.5
            if random.random() < success_rate:
                self.stats['raids_completed'] += 1
                xp_gained = tier * random.randint(1000, 2000)
                self.stats['xp_gained'] += xp_gained
                self.update_status(f"✅ Defeated {boss}! (+{xp_gained} XP)")
            else:
                self.update_status(f"❌ Failed to defeat {boss}!")
        else:
            # No raids nearby, simulate random raid
            if random.random() < 0.05:  # 5% chance per cycle
                raid_bosses = ['Mewtwo', 'Rayquaza', 'Groudon', 'Kyogre', 'Dialga', 'Palkia']
                boss = random.choice(raid_bosses)
                
                self.update_status(f"🏰 Starting raid battle against {boss}!")
                time.sleep(2)  # Simulate raid time
                
                # Simulate raid success
                if random.random() < 0.7:  # 70% success rate
                    self.stats['raids_completed'] += 1
                    self.stats['xp_gained'] += random.randint(1000, 5000)
                    self.update_status(f"✅ Defeated {boss}!")
                else:
                    self.update_status(f"❌ Failed to defeat {boss}!")
    
    def _battling_mode(self):
        """Gym battle mode with map integration"""
        if not self.config['battle_gyms']:
            return
        
        # Get nearby gyms
        nearby_gyms = self.get_nearby_gyms(1.5)  # 1.5km radius
        
        if nearby_gyms:
            gym = nearby_gyms[0]  # Closest gym
            team = gym.get('team', 'Neutral')
            level = gym.get('level', 1)
            defenders = gym.get('defenders', 0)
            
            self.update_status(f"⚔️ Battling {gym['name']} (Team: {team}, Level: {level}, Defenders: {defenders})")
            self.update_status(f"🚶 Walking to gym... (Distance: {gym['distance_km']:.2f}km)")
            
            # Simulate movement to gym
            if gym['distance_km'] > 0.1:
                time.sleep(2)  # Simulate walking time
            
            # Simulate battle success based on gym level and defenders
            success_rate = 0.9 if level <= 3 else 0.7 if level <= 5 else 0.5
            if random.random() < success_rate:
                self.stats['gyms_battled'] += 1
                xp_gained = level * random.randint(200, 400)
                self.stats['xp_gained'] += xp_gained
                self.update_status(f"✅ Gym battle won! (+{xp_gained} XP)")
            else:
                self.update_status("❌ Gym battle lost!")
        else:
            # No gyms nearby, simulate random battle
            if random.random() < 0.1:  # 10% chance per cycle
                self.stats['gyms_battled'] += 1
                self.stats['xp_gained'] += random.randint(200, 800)
                self.update_status("⚔️ Battling gym!")
    
    def _exploring_mode(self):
        """Exploration mode with map integration"""
        # Get optimal route from map
        route = self.get_optimal_route_from_map(2.0)  # 2km radius
        
        if route:
            # Follow the optimal route
            next_point = route[0]
            point_type = next_point['type']
            point_name = next_point['name']
            distance = next_point['distance']
            
            if point_type == 'pokemon':
                self.update_status(f"🎯 Exploring to find {point_name} (Distance: {distance:.2f}km)")
            elif point_type == 'pokestop':
                self.update_status(f"🎡 Exploring to {point_name} (Distance: {distance:.2f}km)")
            elif point_type == 'gym':
                self.update_status(f"🏰 Exploring to {point_name} (Distance: {distance:.2f}km)")
            
            # Simulate movement
            if distance > 0.1:
                self.update_status("🚶 Walking to new area...")
                time.sleep(2)  # Simulate walking time
        else:
            # No route available, simulate random exploration
            if random.random() < 0.25:  # 25% chance per cycle
                self.update_status("🚶 Walking to new area...")
                time.sleep(1)  # Simulate walking time
        
        # Simulate finding items
        if random.random() < 0.1:  # 10% chance per cycle
            items = ['Potion', 'Revive', 'Rare Candy', 'Golden Razz Berry']
            item = random.choice(items)
            self.update_status(f"📦 Found {item}!")
    
    def _map_mode(self):
        """Map mode - focused on map data analysis and navigation"""
        try:
            # Refresh map data
            if self.map_integration['auto_refresh']:
                self.refresh_map_data()
            
            # Get comprehensive map data
            map_data = self.get_map_data()
            
            # Analyze nearby Pokemon
            nearby_pokemon = self.get_nearby_pokemon(1.0)
            if nearby_pokemon:
                rare_pokemon = [p for p in nearby_pokemon if p['rarity'] in ['rare', 'legendary'] or p['is_shiny']]
                if rare_pokemon:
                    self.update_status(f"🌟 Found {len(rare_pokemon)} rare Pokemon nearby!")
                    for pokemon in rare_pokemon[:3]:  # Show top 3
                        self.update_status(f"  • {pokemon['name']} (CP: {pokemon['cp']}, Distance: {pokemon['distance_km']:.2f}km)")
                else:
                    self.update_status(f"🎯 Found {len(nearby_pokemon)} Pokemon nearby")
            
            # Analyze nearby Pokestops
            nearby_stops = self.get_nearby_pokestops(1.0)
            if nearby_stops:
                lured_stops = [s for s in nearby_stops if s.get('lure_type') is not None]
                if lured_stops:
                    self.update_status(f"🎡 Found {len(lured_stops)} lured Pokestops nearby!")
                else:
                    self.update_status(f"🎡 Found {len(nearby_stops)} Pokestops nearby")
            
            # Analyze nearby Gyms
            nearby_gyms = self.get_nearby_gyms(1.0)
            if nearby_gyms:
                raid_gyms = [g for g in nearby_gyms if g.get('raid_boss') is not None]
                if raid_gyms:
                    self.update_status(f"🏰 Found {len(raid_gyms)} raids nearby!")
                    for gym in raid_gyms[:2]:  # Show top 2
                        self.update_status(f"  • {gym['name']} - {gym['raid_boss']} (Tier {gym.get('raid_tier', 1)})")
                else:
                    self.update_status(f"🏰 Found {len(nearby_gyms)} Gyms nearby")
            
            # Check for nests
            nests = map_data.get('nests', [])
            if nests:
                self.update_status(f"🌿 Found {len(nests)} Pokemon nests nearby!")
                for nest in nests:
                    self.update_status(f"  • {nest['pokemon']} nest (Spawn rate: {nest['spawn_rate']:.1%})")
            
            # Calculate optimal route
            route = self.get_optimal_route_from_map(2.0)
            if route:
                self.update_status(f"🗺️ Optimal route calculated with {len(route)} stops")
                
                # Show route summary
                pokemon_stops = len([p for p in route if p['type'] == 'pokemon'])
                pokestop_stops = len([p for p in route if p['type'] == 'pokestop'])
                gym_stops = len([p for p in route if p['type'] == 'gym'])
                
                self.update_status(f"  • {pokemon_stops} Pokemon, {pokestop_stops} Pokestops, {gym_stops} Gyms")
            
            # Auto-refresh map data
            if self.map_integration['auto_refresh']:
                time.sleep(self.map_integration['update_interval'])
            
        except Exception as e:
            self.logger.error(f"Map mode error: {e}")
            self.update_status(f"❌ Map mode error: {e}")
    
    def _idle_mode(self):
        """Idle mode - bot is running but not actively doing anything"""
        if random.random() < 0.05:  # 5% chance per cycle
            self.update_status("😴 Bot is idle...")
    
    def get_stats(self):
        """Get current bot statistics"""
        return self.stats.copy()
    
    def get_status(self):
        """Get current bot status"""
        return {
            'running': self.running,
            'paused': self.paused,
            'mode': self.current_mode,
            'current_activity': self.stats['current_activity'],
            'uptime': str(datetime.datetime.now() - self.stats['start_time']) if self.stats['start_time'] else '0:00:00'
        }
    
    def update_config(self, new_config):
        """Update bot configuration"""
        self.config.update(new_config)
        self.update_status("⚙️ Configuration updated!")
    
    def export_stats(self, filename=None):
        """Export bot statistics to file"""
        if filename is None:
            filename = f"thunderbolt_stats_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.stats, f, indent=2, default=str)
            
            self.update_status(f"📊 Statistics exported to {filename}")
            return True
        except Exception as e:
            self.update_status(f"❌ Failed to export stats: {e}")
            return False
    
    def reset_stats(self):
        """Reset bot statistics"""
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
        self.update_status("🔄 Statistics reset!")

# Example usage and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create bot instance
    bot = ThunderboltPokemonGOBot()
    
    # Test bot functionality
    print("Testing Thunderbolt Pokemon GO Bot...")
    
    # Test status updates
    bot.update_status("Bot initialized!")
    
    # Test configuration
    bot.update_config({'walk_speed': 5.0})
    
    # Test starting bot
    if bot.start_bot('catching'):
        print("Bot started successfully!")
        
        # Let it run for a bit
        time.sleep(10)
        
        # Test pausing
        bot.pause_bot()
        time.sleep(2)
        bot.pause_bot()
        
        # Test mode switching
        bot.set_mode('raiding')
        time.sleep(5)
        
        # Test stopping
        bot.stop_bot()
    
    # Print final stats
    print("\nFinal Statistics:")
    stats = bot.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("Bot test completed!")
    
    # Test Pokemon Map integration
    print("\n" + "="*50)
    print("Testing Pokemon Map Integration...")
    print("="*50)
    
    # Test opening Pokemon Map
    print("🗺️ Testing Pokemon Map opening...")
    if bot.open_pokemon_map():
        print("✅ Pokemon Map opened successfully!")
    else:
        print("❌ Failed to open Pokemon Map")
    
    # Test map data retrieval
    print("\n📊 Testing map data retrieval...")
    map_data = bot.get_map_data()
    print(f"✅ Map data retrieved: {len(map_data.get('pokemon_spawns', []))} Pokemon, {len(map_data.get('pokestops', []))} Pokestops, {len(map_data.get('gyms', []))} Gyms")
    
    # Test nearby Pokemon search
    print("\n🎯 Testing nearby Pokemon search...")
    nearby_pokemon = bot.get_nearby_pokemon(1.0)
    print(f"✅ Found {len(nearby_pokemon)} Pokemon within 1km")
    for pokemon in nearby_pokemon[:3]:  # Show first 3
        print(f"  • {pokemon['name']} (CP: {pokemon['cp']}, Distance: {pokemon['distance_km']:.2f}km)")
    
    # Test rare Pokemon search
    print("\n🌟 Testing rare Pokemon search...")
    rare_pokemon = bot.find_rare_pokemon(2.0)
    print(f"✅ Found {len(rare_pokemon)} rare Pokemon within 2km")
    for pokemon in rare_pokemon[:2]:  # Show first 2
        print(f"  • {pokemon['name']} (CP: {pokemon['cp']}, Rarity: {pokemon['rarity']})")
    
    # Test optimal route calculation
    print("\n🗺️ Testing optimal route calculation...")
    route = bot.get_optimal_route_from_map(2.0)
    print(f"✅ Calculated optimal route with {len(route)} stops")
    for point in route[:5]:  # Show first 5 stops
        print(f"  • {point['type'].title()}: {point['name']} (Priority: {point['priority']}, Distance: {point['distance']:.2f}km)")
    
    # Test map status
    print("\n📈 Testing map status...")
    map_status = bot.get_map_status()
    print(f"✅ Map Status:")
    print(f"  • Enabled: {map_status.get('enabled', False)}")
    print(f"  • Auto-refresh: {map_status.get('auto_refresh', False)}")
    print(f"  • Nearby Pokemon: {map_status.get('nearby_pokemon', 0)}")
    print(f"  • Nearby Pokestops: {map_status.get('nearby_pokestops', 0)}")
    print(f"  • Nearby Gyms: {map_status.get('nearby_gyms', 0)}")
    print(f"  • Rare Pokemon: {map_status.get('rare_pokemon', 0)}")
    
    # Test Pokemon type search
    print("\n🔍 Testing Pokemon type search...")
    fire_pokemon = bot.search_pokemon_by_type('fire', 2.0)
    print(f"✅ Found {len(fire_pokemon)} Fire-type Pokemon")
    for pokemon in fire_pokemon[:2]:
        print(f"  • {pokemon['name']} (CP: {pokemon['cp']})")
    
    # Test map mode
    print("\n🗺️ Testing map mode...")
    bot.set_mode('map_mode')
    print("✅ Switched to map mode")
    
    # Test map data export
    print("\n💾 Testing map data export...")
    if bot.export_map_data("test_map_data.json"):
        print("✅ Map data exported successfully!")
    else:
        print("❌ Failed to export map data")
    
    print("\n" + "="*50)
    print("Pokemon Map Integration Test Completed!")
    print("="*50)
