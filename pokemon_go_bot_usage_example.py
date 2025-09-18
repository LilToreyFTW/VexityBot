
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
