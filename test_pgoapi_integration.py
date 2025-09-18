# -*- coding: utf-8 -*-
"""
Simple pgoapi Integration Test
Tests the pgoapi integration without the problematic existing bot components
"""

import os
import sys
import logging

# ADDED: Add pgoapi to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
pgoapi_path = os.path.join(current_dir, 'pgoapi')
if pgoapi_path not in sys.path:
    sys.path.insert(0, pgoapi_path)

def test_pgoapi_import():
    """Test pgoapi import"""
    try:
        from pgoapi import PGoApi
        from pgoapi.exceptions import AuthException, NotLoggedInException
        from pgoapi.utilities import f2i, get_cell_ids
        print("✅ pgoapi import successful")
        return True
    except ImportError as e:
        print(f"❌ pgoapi import failed: {e}")
        return False

def test_pgoapi_creation():
    """Test pgoapi instance creation"""
    try:
        from pgoapi import PGoApi
        
        # Create pgoapi instance
        api = PGoApi(
            position_lat=40.7589,
            position_lng=-73.9851,
            position_alt=10
        )
        
        print("✅ pgoapi instance creation successful")
        return True
    except Exception as e:
        print(f"❌ pgoapi instance creation failed: {e}")
        return False

def test_enhanced_bot():
    """Test enhanced bot creation"""
    try:
        from Enhanced_PokemonGo_Bot import EnhancedPokemonGoBot
        
        # Create enhanced bot instance
        bot = EnhancedPokemonGoBot()
        
        print("✅ Enhanced bot creation successful")
        return True
    except Exception as e:
        print(f"❌ Enhanced bot creation failed: {e}")
        return False

def test_gui_creation():
    """Test GUI creation"""
    try:
        from Enhanced_PokemonGo_Bot_Integration import EnhancedPokemonGoBotGUI
        
        # Create GUI instance (without running)
        gui = EnhancedPokemonGoBotGUI()
        
        print("✅ GUI creation successful")
        return True
    except Exception as e:
        print(f"❌ GUI creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 pgoapi Integration Test")
    print("=" * 40)
    
    tests = [
        ("pgoapi Import", test_pgoapi_import),
        ("pgoapi Creation", test_pgoapi_creation),
        ("Enhanced Bot", test_enhanced_bot),
        ("GUI Creation", test_gui_creation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        results[test_name] = test_func()
    
    print(f"\n📊 Test Results:")
    print("=" * 40)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! pgoapi integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
