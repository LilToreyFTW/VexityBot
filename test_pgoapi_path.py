#!/usr/bin/env python3
"""
Test script to verify pgoapi path handling in both development and PyInstaller environments
"""

import sys
import os

def test_pgoapi_path():
    """Test pgoapi path resolution"""
    print("Testing pgoapi path resolution...")
    print(f"sys.frozen: {getattr(sys, 'frozen', False)}")
    
    # Handle both development and PyInstaller environments
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        base_path = sys._MEIPASS
        pgoapi_path = os.path.join(base_path, 'pgoapi')
        print(f"PyInstaller mode - base_path: {base_path}")
    else:
        # Running in development
        pgoapi_path = os.path.join(os.getcwd(), 'pgoapi')
        print(f"Development mode - cwd: {os.getcwd()}")
    
    print(f"pgoapi_path: {pgoapi_path}")
    print(f"pgoapi_path exists: {os.path.exists(pgoapi_path)}")
    
    if pgoapi_path not in sys.path and os.path.exists(pgoapi_path):
        sys.path.insert(0, pgoapi_path)
        print(f"Added to sys.path: {pgoapi_path}")
    
    # Test import
    try:
        from pgoapi import PGoApi
        print("✅ pgoapi import successful!")
        return True
    except ImportError as e:
        print(f"❌ pgoapi import failed: {e}")
        return False

def main():
    """Main test function"""
    print("pgoapi Path Test")
    print("=" * 20)
    
    success = test_pgoapi_path()
    
    print("\n" + "=" * 20)
    if success:
        print("✅ Path test passed!")
    else:
        print("❌ Path test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
