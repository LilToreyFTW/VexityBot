# ADDED - Test script for VexityBot Steganography functionality

import os
import sys
from VexityBotSteganography import VexityBotSteganography

def test_steganography():
    """Test the steganography functionality"""
    print("🧪 Testing VexityBot Steganography")
    print("=" * 40)
    
    # Initialize steganography system
    stego = VexityBotSteganography()
    
    # Test image validation
    print("1. Testing image validation...")
    image_path = "imagecoded/momo.png"
    
    if os.path.exists(image_path):
        is_valid, message = stego.validate_image(image_path)
        print(f"   ✅ Image validation: {message}")
        
        max_size = stego.get_max_script_size(image_path)
        print(f"   📏 Max script size: {max_size} bytes")
    else:
        print(f"   ❌ Image not found: {image_path}")
        return False
    
    # Test script creation
    print("\n2. Testing script creation...")
    test_script_content = '''
# Test script for steganography
Write-Host "Hello from hidden script!" -ForegroundColor Green
Write-Host "This script was hidden in an image!" -ForegroundColor Yellow
Get-Date
'''
    
    test_script_path = "test_script.ps1"
    with open(test_script_path, 'w', encoding='utf-8') as f:
        f.write(test_script_content)
    
    print(f"   ✅ Test script created: {test_script_path}")
    
    # Test simple payload creation
    print("\n3. Testing simple payload creation...")
    try:
        output_path = "test_output.png"
        ps_command = stego.create_simple_payload(
            test_script_content, 
            image_path, 
            output_path
        )
        
        if os.path.exists(output_path):
            print(f"   ✅ Simple payload created: {output_path}")
            print(f"   📏 Output size: {os.path.getsize(output_path)} bytes")
        else:
            print("   ❌ Output file not created")
            return False
            
    except Exception as e:
        print(f"   ❌ Simple payload creation failed: {str(e)}")
        return False
    
    # Test advanced payload creation
    print("\n4. Testing advanced payload creation...")
    try:
        advanced_output = "test_advanced_output.png"
        ps_command, batch_path = stego.create_advanced_payload(
            test_script_path,
            image_path,
            advanced_output
        )
        
        if os.path.exists(advanced_output) and os.path.exists(batch_path):
            print(f"   ✅ Advanced payload created: {advanced_output}")
            print(f"   📝 Batch file created: {batch_path}")
        else:
            print("   ❌ Advanced payload files not created")
            return False
            
    except Exception as e:
        print(f"   ❌ Advanced payload creation failed: {str(e)}")
        return False
    
    # Cleanup
    print("\n5. Cleaning up test files...")
    test_files = [test_script_path, output_path, advanced_output, batch_path]
    for file_path in test_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"   🗑️ Removed: {file_path}")
    
    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    success = test_steganography()
    if success:
        print("\n🎉 Steganography module is working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
