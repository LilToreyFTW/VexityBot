#!/usr/bin/env python3
"""
Test script to verify DeathBot integration in main_gui.py
"""

import sys
import os

def test_deathbot_import():
    """Test if DeathBot can be imported"""
    try:
        from DeathBot import DeathBot
        print("✅ DeathBot module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import DeathBot: {e}")
        return False

def test_deathbot_creation():
    """Test if DeathBot can be created"""
    try:
        from DeathBot import DeathBot
        deathbot = DeathBot(bot_id=25, name="DeathBot")
        print("✅ DeathBot instance created successfully")
        print(f"   Bot ID: {deathbot.bot_id}")
        print(f"   Bot Name: {deathbot.name}")
        print(f"   Status: {deathbot.status}")
        return True
    except Exception as e:
        print(f"❌ Failed to create DeathBot: {e}")
        return False

def test_deathbot_config():
    """Test DeathBot configuration"""
    try:
        from DeathBot import DeathBot
        deathbot = DeathBot(bot_id=25, name="DeathBot")
        
        print("✅ DeathBot configuration:")
        print(f"   Destruction Power: {deathbot.config['destruction_power']}")
        print(f"   Countdown Timer: {deathbot.config['countdown_timer']} seconds")
        print(f"   AC Voltage: {deathbot.config['ac_plug_voltage']}")
        print(f"   Ricochet Boom: {deathbot.config['ricochet_boom_mode']}")
        print(f"   Target Directories: {len(deathbot.config['target_directories'])}")
        print(f"   File Extensions: {len(deathbot.config['file_extensions'])}")
        return True
    except Exception as e:
        print(f"❌ Failed to test DeathBot config: {e}")
        return False

def test_deathbot_methods():
    """Test DeathBot methods"""
    try:
        from DeathBot import DeathBot
        deathbot = DeathBot(bot_id=25, name="DeathBot")
        
        # Test status methods
        status = deathbot.get_status()
        stats = deathbot.get_stats()
        
        print("✅ DeathBot methods working:")
        print(f"   Status keys: {list(status.keys())}")
        print(f"   Stats keys: {list(stats.keys())}")
        
        # Test configuration methods
        deathbot.set_destruction_power(75)
        print(f"   Destruction power set to: {deathbot.config['destruction_power']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to test DeathBot methods: {e}")
        return False

def test_main_gui_integration():
    """Test if main_gui.py can be imported with DeathBot integration"""
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import main_gui (this will test the DeathBot integration)
        import main_gui
        print("✅ main_gui.py imported successfully with DeathBot integration")
        
        # Check if DeathBot methods exist
        if hasattr(main_gui.VexityBotGUI, 'initialize_deathbot'):
            print("✅ initialize_deathbot method found")
        else:
            print("❌ initialize_deathbot method not found")
            
        if hasattr(main_gui.VexityBotGUI, 'create_deathbot_tab'):
            print("✅ create_deathbot_tab method found")
        else:
            print("❌ create_deathbot_tab method not found")
            
        if hasattr(main_gui.VexityBotGUI, 'start_deathbot'):
            print("✅ start_deathbot method found")
        else:
            print("❌ start_deathbot method not found")
            
        return True
    except Exception as e:
        print(f"❌ Failed to test main_gui integration: {e}")
        return False

def main():
    """Run all tests"""
    print("💀 DeathBot Integration Test")
    print("=" * 40)
    
    tests = [
        ("DeathBot Import", test_deathbot_import),
        ("DeathBot Creation", test_deathbot_creation),
        ("DeathBot Configuration", test_deathbot_config),
        ("DeathBot Methods", test_deathbot_methods),
        ("Main GUI Integration", test_main_gui_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DeathBot integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
