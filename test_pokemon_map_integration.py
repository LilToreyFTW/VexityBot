#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Pokemon Map integration in Thunderbolt PokemonGO Bot
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Thunderbolt_PokemonGO_Bot import ThunderboltPokemonGOBot

def test_pokemon_map_integration():
    """Test the Pokemon Map integration functionality"""
    print("🗺️ Testing Pokemon Map Integration in Thunderbolt PokemonGO Bot")
    print("=" * 70)
    
    # Create bot instance
    bot = ThunderboltPokemonGOBot()
    
    # Set test location (Times Square, NYC)
    bot.set_location_by_coordinates(40.7589, -73.9851, 10)
    
    print(f"📍 Bot location set to: {bot.config['location']['address']}")
    print(f"   Coordinates: {bot.config['location']['lat']:.6f}, {bot.config['location']['lng']:.6f}")
    
    # Test 1: Open Pokemon Map
    print("\n1. Testing Pokemon Map opening...")
    if bot.open_pokemon_map():
        print("   ✅ Pokemon Map opened successfully!")
    else:
        print("   ❌ Failed to open Pokemon Map")
    
    # Test 2: Get map data
    print("\n2. Testing map data retrieval...")
    map_data = bot.get_map_data()
    pokemon_count = len(map_data.get('pokemon_spawns', []))
    stops_count = len(map_data.get('pokestops', []))
    gyms_count = len(map_data.get('gyms', []))
    nests_count = len(map_data.get('nests', []))
    
    print(f"   ✅ Map data retrieved:")
    print(f"      • Pokemon spawns: {pokemon_count}")
    print(f"      • Pokestops: {stops_count}")
    print(f"      • Gyms: {gyms_count}")
    print(f"      • Nests: {nests_count}")
    
    # Test 3: Find nearby Pokemon
    print("\n3. Testing nearby Pokemon search...")
    nearby_pokemon = bot.get_nearby_pokemon(1.0)  # 1km radius
    print(f"   ✅ Found {len(nearby_pokemon)} Pokemon within 1km")
    
    if nearby_pokemon:
        print("   Top 3 closest Pokemon:")
        for i, pokemon in enumerate(nearby_pokemon[:3], 1):
            print(f"      {i}. {pokemon['name']} (CP: {pokemon['cp']}, Distance: {pokemon['distance_km']:.2f}km)")
    
    # Test 4: Find rare Pokemon
    print("\n4. Testing rare Pokemon search...")
    rare_pokemon = bot.find_rare_pokemon(2.0)  # 2km radius
    print(f"   ✅ Found {len(rare_pokemon)} rare Pokemon within 2km")
    
    if rare_pokemon:
        print("   Rare Pokemon found:")
        for pokemon in rare_pokemon[:3]:
            rarity_emoji = "🌟" if pokemon['is_shiny'] else "💎" if pokemon['rarity'] == 'legendary' else "⭐"
            print(f"      {rarity_emoji} {pokemon['name']} (CP: {pokemon['cp']}, Rarity: {pokemon['rarity']})")
    
    # Test 5: Find nearby Pokestops
    print("\n5. Testing nearby Pokestops search...")
    nearby_stops = bot.get_nearby_pokestops(1.0)
    print(f"   ✅ Found {len(nearby_stops)} Pokestops within 1km")
    
    if nearby_stops:
        print("   Closest Pokestops:")
        for i, stop in enumerate(nearby_stops[:3], 1):
            lure_info = f" (Lured: {stop.get('lure_type', 'None')})" if stop.get('lure_type') else ""
            print(f"      {i}. {stop['name']} (Distance: {stop['distance_km']:.2f}km){lure_info}")
    
    # Test 6: Find nearby Gyms
    print("\n6. Testing nearby Gyms search...")
    nearby_gyms = bot.get_nearby_gyms(1.0)
    print(f"   ✅ Found {len(nearby_gyms)} Gyms within 1km")
    
    if nearby_gyms:
        print("   Closest Gyms:")
        for i, gym in enumerate(nearby_gyms[:3], 1):
            raid_info = f" (Raid: {gym.get('raid_boss', 'None')})" if gym.get('raid_boss') else ""
            print(f"      {i}. {gym['name']} (Team: {gym.get('team', 'Unknown')}, Distance: {gym['distance_km']:.2f}km){raid_info}")
    
    # Test 7: Calculate optimal route
    print("\n7. Testing optimal route calculation...")
    route = bot.get_optimal_route_from_map(2.0)
    print(f"   ✅ Calculated optimal route with {len(route)} stops")
    
    if route:
        print("   Route stops (first 5):")
        for i, point in enumerate(route[:5], 1):
            emoji = "🎯" if point['type'] == 'pokemon' else "🎡" if point['type'] == 'pokestop' else "🏰"
            print(f"      {i}. {emoji} {point['name']} (Priority: {point['priority']}, Distance: {point['distance']:.2f}km)")
    
    # Test 8: Search Pokemon by type
    print("\n8. Testing Pokemon type search...")
    fire_pokemon = bot.search_pokemon_by_type('fire', 2.0)
    water_pokemon = bot.search_pokemon_by_type('water', 2.0)
    electric_pokemon = bot.search_pokemon_by_type('electric', 2.0)
    
    print(f"   ✅ Type search results:")
    print(f"      • Fire-type: {len(fire_pokemon)} Pokemon")
    print(f"      • Water-type: {len(water_pokemon)} Pokemon")
    print(f"      • Electric-type: {len(electric_pokemon)} Pokemon")
    
    if fire_pokemon:
        print("      Fire Pokemon found:")
        for pokemon in fire_pokemon[:2]:
            print(f"         • {pokemon['name']} (CP: {pokemon['cp']})")
    
    # Test 9: Map status
    print("\n9. Testing map status...")
    map_status = bot.get_map_status()
    print(f"   ✅ Map Status:")
    print(f"      • Enabled: {map_status.get('enabled', False)}")
    print(f"      • Auto-refresh: {map_status.get('auto_refresh', False)}")
    print(f"      • Refresh interval: {map_status.get('refresh_interval', 0)}s")
    print(f"      • Last update: {map_status.get('last_update', 'Never')}")
    print(f"      • Nearby Pokemon: {map_status.get('nearby_pokemon', 0)}")
    print(f"      • Nearby Pokestops: {map_status.get('nearby_pokestops', 0)}")
    print(f"      • Nearby Gyms: {map_status.get('nearby_gyms', 0)}")
    print(f"      • Rare Pokemon: {map_status.get('rare_pokemon', 0)}")
    
    # Test 10: Map mode
    print("\n10. Testing map mode...")
    bot.set_mode('map_mode')
    print("    ✅ Switched to map mode")
    
    # Test 11: Export map data
    print("\n11. Testing map data export...")
    if bot.export_map_data("test_pokemon_map_data.json"):
        print("    ✅ Map data exported successfully!")
    else:
        print("    ❌ Failed to export map data")
    
    # Test 12: Map heatmap
    print("\n12. Testing map heatmap generation...")
    heatmap = bot.get_map_heatmap(1.0)
    print(f"    ✅ Generated heatmap with {len(heatmap)} grid cells")
    
    if heatmap:
        print("    Heatmap data (first 3 cells):")
        for i, cell in enumerate(heatmap[:3], 1):
            print(f"       {i}. Cell at ({cell['lat']:.4f}, {cell['lng']:.4f}): {cell['count']} Pokemon")
    
    print("\n" + "=" * 70)
    print("🎉 Pokemon Map Integration Test Completed Successfully!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        test_pokemon_map_integration()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
