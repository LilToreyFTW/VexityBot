# -*- coding: utf-8 -*-
"""
Pokemon Data Manager - Handles Pokemon GO game data
Integrates Pokemon data, moves, types, and game mechanics
"""

import json
import os
import logging
from typing import Dict, List, Optional, Tuple

class PokemonDataManager:
    """Manages Pokemon GO game data including Pokemon, moves, types, and mechanics"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.logger = logging.getLogger(__name__)
        
        # Data storage
        self.pokemon_data = {}
        self.fast_moves = {}
        self.charged_moves = {}
        self.types = {}
        self.items = {}
        self.level_to_cpm = {}
        self.xp_per_level = {}
        self.pokemon_upgrade_cost = {}
        
        # Load all data
        self.load_all_data()
    
    def load_all_data(self):
        """Load all Pokemon GO data files"""
        try:
            self.load_pokemon_data()
            self.load_moves_data()
            self.load_types_data()
            self.load_items_data()
            self.load_level_data()
            self.load_xp_data()
            self.load_upgrade_cost_data()
            self.logger.info("All Pokemon GO data loaded successfully!")
        except Exception as e:
            self.logger.error(f"Failed to load Pokemon data: {e}")
    
    def load_pokemon_data(self):
        """Load Pokemon data from pokemon.json"""
        try:
            pokemon_file = os.path.join(self.data_dir, "pokemon.json")
            if os.path.exists(pokemon_file):
                with open(pokemon_file, 'r', encoding='utf-8') as f:
                    pokemon_list = json.load(f)
                
                for pokemon in pokemon_list:
                    self.pokemon_data[pokemon['Number']] = pokemon
                    self.pokemon_data[pokemon['Name'].lower()] = pokemon
                
                self.logger.info(f"Loaded {len(pokemon_list)} Pokemon")
            else:
                self.logger.warning("pokemon.json not found, using default data")
                self._create_default_pokemon_data()
        except Exception as e:
            self.logger.error(f"Failed to load Pokemon data: {e}")
            self._create_default_pokemon_data()
    
    def load_moves_data(self):
        """Load moves data from fast_moves.json and charged_moves.json"""
        try:
            # Load fast moves
            fast_moves_file = os.path.join(self.data_dir, "fast_moves.json")
            if os.path.exists(fast_moves_file):
                with open(fast_moves_file, 'r', encoding='utf-8') as f:
                    fast_moves_list = json.load(f)
                
                for move in fast_moves_list:
                    self.fast_moves[move['name']] = move
                
                self.logger.info(f"Loaded {len(fast_moves_list)} fast moves")
            
            # Load charged moves
            charged_moves_file = os.path.join(self.data_dir, "charged_moves.json")
            if os.path.exists(charged_moves_file):
                with open(charged_moves_file, 'r', encoding='utf-8') as f:
                    charged_moves_list = json.load(f)
                
                for move in charged_moves_list:
                    self.charged_moves[move['name']] = move
                
                self.logger.info(f"Loaded {len(charged_moves_list)} charged moves")
        except Exception as e:
            self.logger.error(f"Failed to load moves data: {e}")
    
    def load_types_data(self):
        """Load Pokemon types data from types.json"""
        try:
            types_file = os.path.join(self.data_dir, "types.json")
            if os.path.exists(types_file):
                with open(types_file, 'r', encoding='utf-8') as f:
                    types_list = json.load(f)
                
                for type_data in types_list:
                    self.types[type_data['name']] = type_data
                
                self.logger.info(f"Loaded {len(types_list)} types")
        except Exception as e:
            self.logger.error(f"Failed to load types data: {e}")
    
    def load_items_data(self):
        """Load items data from items.json"""
        try:
            items_file = os.path.join(self.data_dir, "items.json")
            if os.path.exists(items_file):
                with open(items_file, 'r', encoding='utf-8') as f:
                    self.items = json.load(f)
                self.logger.info("Loaded items data")
        except Exception as e:
            self.logger.error(f"Failed to load items data: {e}")
    
    def load_level_data(self):
        """Load level to CP multiplier data"""
        try:
            level_file = os.path.join(self.data_dir, "level_to_cpm.json")
            if os.path.exists(level_file):
                with open(level_file, 'r', encoding='utf-8') as f:
                    self.level_to_cpm = json.load(f)
                self.logger.info("Loaded level to CP multiplier data")
        except Exception as e:
            self.logger.error(f"Failed to load level data: {e}")
    
    def load_xp_data(self):
        """Load XP per level data"""
        try:
            xp_file = os.path.join(self.data_dir, "xp_per_level.json")
            if os.path.exists(xp_file):
                with open(xp_file, 'r', encoding='utf-8') as f:
                    self.xp_per_level = json.load(f)
                self.logger.info("Loaded XP per level data")
        except Exception as e:
            self.logger.error(f"Failed to load XP data: {e}")
    
    def load_upgrade_cost_data(self):
        """Load Pokemon upgrade cost data"""
        try:
            upgrade_file = os.path.join(self.data_dir, "pokemon_upgrade_cost.json")
            if os.path.exists(upgrade_file):
                with open(upgrade_file, 'r', encoding='utf-8') as f:
                    self.pokemon_upgrade_cost = json.load(f)
                self.logger.info("Loaded Pokemon upgrade cost data")
        except Exception as e:
            self.logger.error(f"Failed to load upgrade cost data: {e}")
    
    def _create_default_pokemon_data(self):
        """Create default Pokemon data if files are not available"""
        self.pokemon_data = {
            "001": {
                "Number": "001",
                "Name": "Bulbasaur",
                "Type I": ["Grass"],
                "Type II": ["Poison"],
                "BaseAttack": 118,
                "BaseDefense": 118,
                "BaseStamina": 90,
                "CaptureRate": 0.2,
                "FleeRate": 0.1,
                "Fast Attack(s)": ["Vine Whip", "Tackle"],
                "Special Attack(s)": ["Sludge Bomb", "Seed Bomb", "Power Whip"]
            },
            "150": {
                "Number": "150",
                "Name": "Mewtwo",
                "Type I": ["Psychic"],
                "Type II": [],
                "BaseAttack": 300,
                "BaseDefense": 182,
                "BaseStamina": 193,
                "CaptureRate": 0.05,
                "FleeRate": 0.05,
                "Fast Attack(s)": ["Psycho Cut", "Confusion"],
                "Special Attack(s)": ["Psychic", "Shadow Ball", "Focus Blast"]
            }
        }
    
    def get_pokemon(self, identifier: str) -> Optional[Dict]:
        """Get Pokemon data by number or name"""
        return self.pokemon_data.get(identifier) or self.pokemon_data.get(identifier.lower())
    
    def get_pokemon_by_type(self, type_name: str) -> List[Dict]:
        """Get all Pokemon of a specific type"""
        pokemon_list = []
        for pokemon in self.pokemon_data.values():
            if isinstance(pokemon, dict):
                if (pokemon.get('Type I') and type_name in pokemon['Type I']) or \
                   (pokemon.get('Type II') and type_name in pokemon['Type II']):
                    pokemon_list.append(pokemon)
        return pokemon_list
    
    def get_legendary_pokemon(self) -> List[Dict]:
        """Get all Legendary Pokemon"""
        legendary_numbers = ["144", "145", "146", "150", "151", "243", "244", "245", "249", "250", "251"]
        legendary_pokemon = []
        for number in legendary_numbers:
            pokemon = self.get_pokemon(number)
            if pokemon:
                legendary_pokemon.append(pokemon)
        return legendary_pokemon
    
    def get_mythical_pokemon(self) -> List[Dict]:
        """Get all Mythical Pokemon"""
        mythical_numbers = ["151", "251", "385", "386", "489", "490", "491", "492", "493", "494", "647", "648", "649"]
        mythical_pokemon = []
        for number in mythical_numbers:
            pokemon = self.get_pokemon(number)
            if pokemon:
                mythical_pokemon.append(pokemon)
        return mythical_pokemon
    
    def get_move_effectiveness(self, attack_type: str, defense_types: List[str]) -> float:
        """Calculate move effectiveness against Pokemon types"""
        if attack_type not in self.types:
            return 1.0
        
        effectiveness = 1.0
        attack_type_data = self.types[attack_type]
        
        for defense_type in defense_types:
            if defense_type in attack_type_data['effectiveAgainst']:
                effectiveness *= 2.0
            elif defense_type in attack_type_data['weakAgainst']:
                effectiveness *= 0.5
        
        return effectiveness
    
    def get_best_moveset(self, pokemon_name: str) -> Dict:
        """Get the best moveset for a Pokemon"""
        pokemon = self.get_pokemon(pokemon_name)
        if not pokemon:
            return {}
        
        # This is a simplified version - in reality, you'd calculate DPS
        fast_attacks = pokemon.get('Fast Attack(s)', [])
        special_attacks = pokemon.get('Special Attack(s)', [])
        
        best_fast = fast_attacks[0] if fast_attacks else "Unknown"
        best_charged = special_attacks[0] if special_attacks else "Unknown"
        
        return {
            'fast_attack': best_fast,
            'charged_attack': best_charged,
            'pokemon': pokemon['Name']
        }
    
    def calculate_cp(self, pokemon_name: str, level: int, attack_iv: int = 15, defense_iv: int = 15, stamina_iv: int = 15) -> int:
        """Calculate CP for a Pokemon at given level and IVs"""
        pokemon = self.get_pokemon(pokemon_name)
        if not pokemon or str(level) not in self.level_to_cpm:
            return 0
        
        cpm = self.level_to_cpm[str(level)]
        base_attack = pokemon.get('BaseAttack', 0)
        base_defense = pokemon.get('BaseDefense', 0)
        base_stamina = pokemon.get('BaseStamina', 0)
        
        attack = (base_attack + attack_iv) * cpm
        defense = (base_defense + defense_iv) * cpm
        stamina = (base_stamina + stamina_iv) * cpm
        
        cp = int(attack * (defense ** 0.5) * (stamina ** 0.5) / 10)
        return max(10, cp)  # Minimum CP is 10
    
    def get_pokemon_stats(self, pokemon_name: str) -> Dict:
        """Get comprehensive stats for a Pokemon"""
        pokemon = self.get_pokemon(pokemon_name)
        if not pokemon:
            return {}
        
        return {
            'name': pokemon.get('Name', 'Unknown'),
            'number': pokemon.get('Number', '000'),
            'types': pokemon.get('Type I', []) + pokemon.get('Type II', []),
            'base_attack': pokemon.get('BaseAttack', 0),
            'base_defense': pokemon.get('BaseDefense', 0),
            'base_stamina': pokemon.get('BaseStamina', 0),
            'capture_rate': pokemon.get('CaptureRate', 0.2),
            'flee_rate': pokemon.get('FleeRate', 0.1),
            'fast_attacks': pokemon.get('Fast Attack(s)', []),
            'charged_attacks': pokemon.get('Special Attack(s)', []),
            'weight': pokemon.get('Weight', 'Unknown'),
            'height': pokemon.get('Height', 'Unknown'),
            'candy_name': pokemon.get('Candy', {}).get('Name', 'Unknown'),
            'buddy_distance': pokemon.get('BuddyDistanceNeeded', 3)
        }
    
    def search_pokemon(self, query: str) -> List[Dict]:
        """Search for Pokemon by name or number"""
        results = []
        query_lower = query.lower()
        
        for pokemon in self.pokemon_data.values():
            if isinstance(pokemon, dict):
                name = pokemon.get('Name', '').lower()
                number = pokemon.get('Number', '')
                
                if query_lower in name or query_lower in number:
                    results.append(pokemon)
        
        return results
    
    def get_type_effectiveness_chart(self) -> Dict:
        """Get type effectiveness chart"""
        chart = {}
        for type_name, type_data in self.types.items():
            chart[type_name] = {
                'effective_against': type_data.get('effectiveAgainst', []),
                'weak_against': type_data.get('weakAgainst', [])
            }
        return chart
    
    def get_all_pokemon_names(self) -> List[str]:
        """Get list of all Pokemon names"""
        names = []
        for pokemon in self.pokemon_data.values():
            if isinstance(pokemon, dict) and 'Name' in pokemon:
                names.append(pokemon['Name'])
        return sorted(names)
    
    def get_pokemon_by_cp_range(self, min_cp: int, max_cp: int, level: int = 40) -> List[Dict]:
        """Get Pokemon within a CP range at a specific level"""
        pokemon_in_range = []
        
        for pokemon in self.pokemon_data.values():
            if isinstance(pokemon, dict):
                cp = self.calculate_cp(pokemon['Name'], level)
                if min_cp <= cp <= max_cp:
                    pokemon_in_range.append({
                        'pokemon': pokemon,
                        'cp': cp
                    })
        
        return sorted(pokemon_in_range, key=lambda x: x['cp'], reverse=True)

# Example usage and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create data manager
    data_manager = PokemonDataManager()
    
    # Test Pokemon lookup
    print("Testing Pokemon Data Manager...")
    
    # Get Mewtwo data
    mewtwo = data_manager.get_pokemon("Mewtwo")
    if mewtwo:
        print(f"Mewtwo: {mewtwo['Name']} - Attack: {mewtwo['BaseAttack']}")
    
    # Get legendary Pokemon
    legendary = data_manager.get_legendary_pokemon()
    print(f"Found {len(legendary)} legendary Pokemon")
    
    # Calculate CP
    cp = data_manager.calculate_cp("Mewtwo", 40, 15, 15, 15)
    print(f"Mewtwo CP at level 40: {cp}")
    
    # Search Pokemon
    results = data_manager.search_pokemon("char")
    print(f"Pokemon containing 'char': {[p['Name'] for p in results[:5]]}")
    
    print("Pokemon Data Manager test completed!")
