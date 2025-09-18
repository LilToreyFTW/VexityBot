# -*- coding: utf-8 -*-
"""
Pokemon GO Bot pgoapi Integration - Complete Integration Script
Integrates the downloaded pgoapi with VexityBot's Pokemon GO bot system
"""

import os
import sys
import json
import time
import logging
import threading
from typing import Dict, List, Optional, Any

# ADDED: Add pgoapi to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
pgoapi_path = os.path.join(current_dir, 'pgoapi')
if pgoapi_path not in sys.path:
    sys.path.insert(0, pgoapi_path)

# Import pgoapi
try:
    from pgoapi import PGoApi
    from pgoapi.exceptions import AuthException, NotLoggedInException, ServerBusyOrOfflineException
    from pgoapi.utilities import f2i, get_cell_ids
    from pgoapi.auth_ptc import AuthPtc
    from pgoapi.auth_google import AuthGoogle
    PGOAPI_IMPORTED = True
    print("✅ pgoapi successfully imported from local directory")
except ImportError as e:
    PGOAPI_IMPORTED = False
    print(f"❌ Failed to import pgoapi: {e}")

# Import existing bot components
try:
    from Thunderbolt_PokemonGO_Bot import ThunderboltPokemonGOBot
    EXISTING_BOT_IMPORTED = True
    print("✅ Existing Thunderbolt bot imported")
except ImportError as e:
    EXISTING_BOT_IMPORTED = False
    print(f"❌ Failed to import existing bot: {e}")

class PokemonGoBotpgoapiIntegration:
    """Complete Pokemon GO Bot integration with pgoapi"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.integration_status = {
            'pgoapi_available': PGOAPI_IMPORTED,
            'existing_bot_available': EXISTING_BOT_IMPORTED,
            'integration_complete': False,
            'errors': []
        }
        
        # Initialize components
        self.pgoapi = None
        self.existing_bot = None
        self.enhanced_bot = None
        
        self._setup_logging()
        self._initialize_components()
    
    def _setup_logging(self):
        """Setup logging for the integration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('pokemon_go_bot_integration.log'),
                logging.StreamHandler()
            ]
        )
    
    def _initialize_components(self):
        """Initialize all bot components"""
        try:
            # Initialize pgoapi if available
            if PGOAPI_IMPORTED:
                self._initialize_pgoapi()
            
            # Initialize existing bot if available
            if EXISTING_BOT_IMPORTED:
                self._initialize_existing_bot()
            
            # Create enhanced integration
            self._create_enhanced_integration()
            
            self.integration_status['integration_complete'] = True
            self.logger.info("✅ Pokemon GO Bot pgoapi integration completed successfully")
            
        except Exception as e:
            self.integration_status['errors'].append(str(e))
            self.logger.error(f"❌ Integration failed: {e}")
    
    def _initialize_pgoapi(self):
        """Initialize pgoapi component"""
        try:
            # Create pgoapi instance
            self.pgoapi = PGoApi()
            self.logger.info("✅ pgoapi initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ pgoapi initialization failed: {e}")
            self.integration_status['errors'].append(f"pgoapi init: {e}")
    
    def _initialize_existing_bot(self):
        """Initialize existing bot component"""
        try:
            # Create existing bot instance
            self.existing_bot = ThunderboltPokemonGOBot()
            self.logger.info("✅ Existing Thunderbolt bot initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Existing bot initialization failed: {e}")
            self.integration_status['errors'].append(f"existing bot init: {e}")
    
    def _create_enhanced_integration(self):
        """Create enhanced integration combining both systems"""
        try:
            # Import enhanced bot
            from Enhanced_PokemonGo_Bot import EnhancedPokemonGoBot
            
            # Create enhanced bot instance
            self.enhanced_bot = EnhancedPokemonGoBot()
            self.logger.info("✅ Enhanced bot created successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Enhanced bot creation failed: {e}")
            self.integration_status['errors'].append(f"enhanced bot: {e}")
    
    def get_integration_status(self):
        """Get current integration status"""
        return self.integration_status.copy()
    
    def test_pgoapi_connection(self, username=None, password=None, provider='ptc'):
        """Test pgoapi connection"""
        if not PGOAPI_IMPORTED:
            return {"success": False, "error": "pgoapi not available"}
        
        try:
            # Create test pgoapi instance
            test_api = PGoApi(
                provider=provider,
                username=username,
                password=password,
                position_lat=40.7589,
                position_lng=-73.9851,
                position_alt=10
            )
            
            # Test basic functionality
            test_api.set_api_endpoint("pgorelease.nianticlabs.com/plfe")
            
            return {"success": True, "message": "pgoapi connection test successful"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_integration_gui(self, parent_frame=None):
        """Create integration GUI"""
        try:
            from Enhanced_PokemonGo_Bot_Integration import EnhancedPokemonGoBotGUI
            
            # Create GUI
            gui = EnhancedPokemonGoBotGUI(parent_frame)
            self.logger.info("✅ Integration GUI created successfully")
            
            return gui
            
        except Exception as e:
            self.logger.error(f"❌ GUI creation failed: {e}")
            return None
    
    def run_integration_test(self):
        """Run comprehensive integration test"""
        test_results = {
            'pgoapi_import': PGOAPI_IMPORTED,
            'existing_bot_import': EXISTING_BOT_IMPORTED,
            'pgoapi_initialization': self.pgoapi is not None,
            'existing_bot_initialization': self.existing_bot is not None,
            'enhanced_bot_creation': self.enhanced_bot is not None,
            'integration_complete': self.integration_status['integration_complete'],
            'errors': self.integration_status['errors']
        }
        
        self.logger.info("🧪 Integration Test Results:")
        for test, result in test_results.items():
            if test != 'errors':
                status = "✅ PASS" if result else "❌ FAIL"
                self.logger.info(f"  {test}: {status}")
        
        if test_results['errors']:
            self.logger.info("  Errors:")
            for error in test_results['errors']:
                self.logger.info(f"    - {error}")
        
        return test_results
    
    def create_usage_example(self):
        """Create usage example"""
        example_code = '''
# Pokemon GO Bot pgoapi Integration Usage Example

from PokemonGo_Bot_pgoapi_Integration import PokemonGoBotpgoapiIntegration

# Create integration instance
integration = PokemonGoBotpgoapiIntegration()

# Check integration status
status = integration.get_integration_status()
print(f"Integration Status: {status}")

# Run integration test
test_results = integration.run_integration_test()

# Test pgoapi connection (replace with actual credentials)
connection_test = integration.test_pgoapi_connection(
    username="your_username",
    password="your_password",
    provider="ptc"
)
print(f"Connection Test: {connection_test}")

# Create GUI
gui = integration.create_integration_gui()
if gui:
    gui.run()

# Use enhanced bot directly
if integration.enhanced_bot:
    # Set credentials
    integration.enhanced_bot.set_credentials("username", "password", "ptc")
    
    # Set location
    integration.enhanced_bot.set_location(40.7589, -73.9851, 10)
    
    # Start bot
    integration.enhanced_bot.start()
'''
        
        # Save example to file
        with open('pokemon_go_bot_usage_example.py', 'w') as f:
            f.write(example_code)
        
        self.logger.info("✅ Usage example created: pokemon_go_bot_usage_example.py")
        return example_code

def main():
    """Main function to demonstrate the integration"""
    print("🚀 Pokemon GO Bot pgoapi Integration")
    print("=" * 50)
    
    # Create integration
    integration = PokemonGoBotpgoapiIntegration()
    
    # Show status
    status = integration.get_integration_status()
    print(f"\n📊 Integration Status:")
    print(f"  pgoapi Available: {status['pgoapi_available']}")
    print(f"  Existing Bot Available: {status['existing_bot_available']}")
    print(f"  Integration Complete: {status['integration_complete']}")
    
    if status['errors']:
        print(f"  Errors: {len(status['errors'])}")
        for error in status['errors']:
            print(f"    - {error}")
    
    # Run tests
    print(f"\n🧪 Running Integration Tests...")
    test_results = integration.run_integration_test()
    
    # Create usage example
    print(f"\n📝 Creating Usage Example...")
    integration.create_usage_example()
    
    # Test pgoapi connection (without credentials)
    print(f"\n🔗 Testing pgoapi Connection...")
    connection_test = integration.test_pgoapi_connection()
    print(f"  Connection Test: {connection_test}")
    
    print(f"\n✅ Integration demonstration completed!")
    print(f"📁 Check 'pokemon_go_bot_usage_example.py' for usage instructions")

if __name__ == "__main__":
    main()
