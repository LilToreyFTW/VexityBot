#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Pokemon Go Bot REST API Integration
Demonstrates all the REST API endpoints and functionality
"""

import time
import logging
import requests
from PokemonGoBot_SpringBoot_Integration import PokemonGoBotSpringBootIntegration

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def gui_callback(message):
    print(f"[GUI_UPDATE] {message}")

def test_rest_api_integration():
    """Test the complete REST API integration"""
    print("Pokemon Go Bot REST API Integration Test")
    print("=" * 50)
    
    # Create integration instance
    integration = PokemonGoBotSpringBootIntegration(gui_callback=gui_callback)
    
    # Test 1: Check Spring Boot status
    print("\n1. Testing Spring Boot Backend Status...")
    status = integration.get_integration_status()
    print(f"   Spring Boot running: {status['spring_boot_running']}")
    print(f"   Integration enabled: {status['integration_enabled']}")
    print(f"   Base URL: {status['base_url']}")
    
    # Test 2: Register a test bot
    print("\n2. Testing Bot Registration...")
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
        },
        'settings': {
            'walk_speed': 4.16,
            'catch_pokemon': True,
            'spin_pokestops': True,
            'battle_gyms': False
        }
    }
    
    if integration.register_bot('test_bot', test_config):
        print("   ✅ Bot registered successfully")
    else:
        print("   ❌ Bot registration failed")
    
    # Test 3: Set bot password and authenticate
    print("\n3. Testing Bot Authentication...")
    test_password = "secure_password_123"
    integration.set_bot_password('test_bot', test_password)
    
    if integration.authenticate_bot('test_bot', test_password):
        print("   ✅ Bot authenticated successfully")
    else:
        print("   ❌ Bot authentication failed")
    
    # Test 4: Bot control operations
    print("\n4. Testing Bot Control Operations...")
    
    # Load bot
    if integration.load_bot('test_bot'):
        print("   ✅ Bot loaded successfully")
    else:
        print("   ❌ Bot load failed")
    
    # Start bot
    if integration.start_bot('test_bot'):
        print("   ✅ Bot started successfully")
    else:
        print("   ❌ Bot start failed")
    
    time.sleep(2)  # Wait a bit
    
    # Stop bot
    if integration.stop_bot('test_bot'):
        print("   ✅ Bot stopped successfully")
    else:
        print("   ❌ Bot stop failed")
    
    # Unload bot
    if integration.unload_bot('test_bot'):
        print("   ✅ Bot unloaded successfully")
    else:
        print("   ❌ Bot unload failed")
    
    # Test 5: Pokemon management (simulated)
    print("\n5. Testing Pokemon Management...")
    
    # Start bot again for Pokemon operations
    integration.load_bot('test_bot')
    integration.start_bot('test_bot')
    
    # Get Pokemon list
    pokemon_data = integration.get_pokemons('test_bot')
    if 'error' not in pokemon_data:
        print("   ✅ Pokemon data retrieved successfully")
        print(f"   Pokemon count: {len(pokemon_data.get('pokemons', []))}")
    else:
        print(f"   ❌ Pokemon data retrieval failed: {pokemon_data['error']}")
    
    # Test Pokemon operations (these will fail in simulation but test the API)
    print("   Testing Pokemon transfer...")
    integration.transfer_pokemon('test_bot', 'test_pokemon_id')
    
    print("   Testing Pokemon evolution...")
    integration.evolve_pokemon('test_bot', 'test_pokemon_id')
    
    print("   Testing Pokemon power up...")
    integration.powerup_pokemon('test_bot', 'test_pokemon_id')
    
    print("   Testing Pokemon favorite toggle...")
    integration.toggle_pokemon_favorite('test_bot', 'test_pokemon_id')
    
    print("   Testing Pokemon rename...")
    integration.rename_pokemon('test_bot', 'test_pokemon_id', 'NewName')
    
    # Test 6: Item management
    print("\n6. Testing Item Management...")
    
    # Get items
    item_data = integration.get_items('test_bot')
    if 'error' not in item_data:
        print("   ✅ Item data retrieved successfully")
        print(f"   Item count: {len(item_data.get('items', []))}")
    else:
        print(f"   ❌ Item data retrieval failed: {item_data['error']}")
    
    # Test item operations
    print("   Testing item drop...")
    integration.drop_item('test_bot', 'test_item_id', 5)
    
    print("   Testing incense use...")
    integration.use_incense('test_bot')
    
    print("   Testing lucky egg use...")
    integration.use_lucky_egg('test_bot')
    
    # Test 7: Location and profile management
    print("\n7. Testing Location and Profile Management...")
    
    # Get location
    location_data = integration.get_location('test_bot')
    if 'error' not in location_data:
        print("   ✅ Location data retrieved successfully")
        print(f"   Location: {location_data}")
    else:
        print(f"   ❌ Location data retrieval failed: {location_data['error']}")
    
    # Set location
    if integration.set_location('test_bot', 40.7128, -74.0060):
        print("   ✅ Location set successfully")
    else:
        print("   ❌ Location set failed")
    
    # Get profile
    profile_data = integration.get_profile('test_bot')
    if 'error' not in profile_data:
        print("   ✅ Profile data retrieved successfully")
    else:
        print(f"   ❌ Profile data retrieval failed: {profile_data['error']}")
    
    # Get pokedex
    pokedex_data = integration.get_pokedex('test_bot')
    if 'error' not in pokedex_data:
        print("   ✅ Pokedex data retrieved successfully")
    else:
        print(f"   ❌ Pokedex data retrieval failed: {pokedex_data['error']}")
    
    # Get eggs
    eggs_data = integration.get_eggs('test_bot')
    if 'error' not in eggs_data:
        print("   ✅ Eggs data retrieved successfully")
    else:
        print(f"   ❌ Eggs data retrieval failed: {eggs_data['error']}")
    
    # Test 8: Statistics
    print("\n8. Testing Statistics...")
    stats = integration.get_statistics()
    print(f"   Total bots: {stats['total_bots']}")
    print(f"   Active bots: {stats['active_bots']}")
    print(f"   Pokemon caught: {stats['pokemon_caught']}")
    print(f"   XP gained: {stats['xp_gained']}")
    
    # Test 9: All bots status
    print("\n9. Testing All Bots Status...")
    all_status = integration.get_all_bots_status()
    if 'error' not in all_status:
        print("   ✅ All bots status retrieved successfully")
        print(f"   Bots: {list(all_status.get('bots', {}).keys())}")
    else:
        print(f"   ❌ All bots status retrieval failed: {all_status['error']}")
    
    # Test 10: Bot reload
    print("\n10. Testing Bot Reload...")
    if integration.reload_bot('test_bot'):
        print("   ✅ Bot reloaded successfully")
    else:
        print("   ❌ Bot reload failed")
    
    # Cleanup
    print("\n11. Cleaning up...")
    integration.stop_bot('test_bot')
    integration.unload_bot('test_bot')
    integration.cleanup()
    
    print("\n" + "=" * 50)
    print("Pokemon Go Bot REST API Integration Test Completed!")
    print("=" * 50)

def test_direct_rest_api_calls():
    """Test direct REST API calls to demonstrate the API structure"""
    print("\nDirect REST API Call Examples")
    print("=" * 40)
    
    base_url = "http://localhost:8080"
    
    # Example 1: Get all bots (no authentication required)
    print("\n1. GET /api/bots (no auth required)")
    try:
        response = requests.get(f"{base_url}/api/bots", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Authenticate with bot
    print("\n2. POST /api/bot/test_bot/auth")
    try:
        password = "secure_password_123"
        response = requests.post(
            f"{base_url}/api/bot/test_bot/auth",
            data=password,  # Raw data, not JSON
            headers={'Content-Type': 'text/plain'},
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data.get('token')
            print(f"   Token: {token}")
            
            # Example 3: Use token for authenticated request
            print("\n3. GET /api/bot/test_bot/pokemons (with auth)")
            headers = {'X-PGB-ACCESS-TOKEN': token}
            response = requests.get(f"{base_url}/api/bot/test_bot/pokemons", headers=headers, timeout=5)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
            else:
                print(f"   Error: {response.text}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

def main():
    """Main test function"""
    print("Pokemon Go Bot REST API Test Suite")
    print("=" * 50)
    
    # Test integration
    test_rest_api_integration()
    
    # Test direct API calls
    test_direct_rest_api_calls()
    
    print("\nTest suite completed!")

if __name__ == "__main__":
    main()
