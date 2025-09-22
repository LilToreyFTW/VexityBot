#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Image Steganography System
Hides client executable within image files for hidden deployment.
"""

import os
import sys
import struct
import base64
import zlib
from PIL import Image
import io

class TSMImageSteganography:
    def __init__(self):
        self.magic_header = b"TSM_SENIOR_OASIS_PANEL"
        self.version = 1
        self.compression_level = 6

    def _encode_data_in_image(self, image_data, payload_data):
        """Encode payload data into image using LSB steganography"""
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            pixels = list(img.getdata())
            
            # Compress payload data
            compressed_payload = zlib.compress(payload_data, self.compression_level)
            
            # Create header with metadata
            header = struct.pack('>I', len(compressed_payload))  # 4 bytes for payload length
            total_data = self.magic_header + header + compressed_payload
            
            # Check if image can hold the data
            max_capacity = (width * height * 3) // 8  # 3 bits per pixel for LSB
            if len(total_data) > max_capacity:
                raise ValueError(f"Image too small to hold data. Max capacity: {max_capacity} bytes, need: {len(total_data)} bytes")
            
            # Encode data using LSB steganography
            data_bits = ''.join(format(byte, '08b') for byte in total_data)
            data_index = 0
            
            new_pixels = []
            for i, pixel in enumerate(pixels):
                r, g, b = pixel
                
                if data_index < len(data_bits):
                    # Modify LSB of each color channel
                    r = (r & 0xFE) | int(data_bits[data_index]) if data_index < len(data_bits) else r
                    data_index += 1
                    
                    g = (g & 0xFE) | int(data_bits[data_index]) if data_index < len(data_bits) else g
                    data_index += 1
                    
                    b = (b & 0xFE) | int(data_bits[data_index]) if data_index < len(data_bits) else b
                    data_index += 1
                
                new_pixels.append((r, g, b))
            
            # Create new image with modified pixels
            new_img = Image.new('RGB', (width, height))
            new_img.putdata(new_pixels)
            
            # Save to bytes
            output = io.BytesIO()
            new_img.save(output, format='PNG')
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f"Error encoding data in image: {e}")

    def _decode_data_from_image(self, image_data):
        """Decode payload data from image using LSB steganography"""
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            width, height = img.size
            pixels = list(img.getdata())
            
            # Extract LSBs from pixels
            bits = []
            for pixel in pixels:
                r, g, b = pixel
                bits.append(str(r & 1))
                bits.append(str(g & 1))
                bits.append(str(b & 1))
            
            # Convert bits to bytes
            data_bytes = []
            for i in range(0, len(bits), 8):
                if i + 8 <= len(bits):
                    byte_bits = ''.join(bits[i:i+8])
                    data_bytes.append(int(byte_bits, 2))
            
            data = bytes(data_bytes)
            
            # Check for magic header
            if not data.startswith(self.magic_header):
                raise ValueError("No TSM data found in image")
            
            # Extract payload length
            header_start = len(self.magic_header)
            payload_length = struct.unpack('>I', data[header_start:header_start+4])[0]
            
            # Extract and decompress payload
            payload_start = header_start + 4
            compressed_payload = data[payload_start:payload_start + payload_length]
            payload = zlib.decompress(compressed_payload)
            
            return payload
            
        except Exception as e:
            raise Exception(f"Error decoding data from image: {e}")

    def embed_client_in_image(self, image_path, client_path, output_path):
        """Embed client executable in an image file"""
        try:
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Read client executable
            with open(client_path, 'rb') as f:
                client_data = f.read()
            
            # Encode client data in image
            stego_image = self._encode_data_in_image(image_data, client_data)
            
            # Save steganographic image
            with open(output_path, 'wb') as f:
                f.write(stego_image)
            
            print(f"TSM-SeniorOasisPanel: Client embedded in image: {output_path}")
            return True
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Error embedding client: {e}")
            return False

    def extract_client_from_image(self, stego_image_path, output_path):
        """Extract client executable from steganographic image"""
        try:
            # Read steganographic image
            with open(stego_image_path, 'rb') as f:
                image_data = f.read()
            
            # Decode client data
            client_data = self._decode_data_from_image(image_data)
            
            # Save extracted client
            with open(output_path, 'wb') as f:
                f.write(client_data)
            
            print(f"TSM-SeniorOasisPanel: Client extracted from image: {output_path}")
            return True
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Error extracting client: {e}")
            return False

    def create_hidden_image(self, original_image_path, client_path, output_path):
        """Create a hidden image that appears normal but contains the client"""
        return self.embed_client_in_image(original_image_path, client_path, output_path)

    def verify_stego_image(self, stego_image_path):
        """Verify if an image contains hidden TSM data"""
        try:
            with open(stego_image_path, 'rb') as f:
                image_data = f.read()
            
            # Try to decode data
            self._decode_data_from_image(image_data)
            print("TSM-SeniorOasisPanel: Image contains valid TSM data")
            return True
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Image does not contain TSM data: {e}")
            return False

def main():
    """Main function for steganography operations"""
    if len(sys.argv) < 4:
        print("Usage:")
        print("  Embed: python TSM_ImageSteganography.py embed <image> <client> <output>")
        print("  Extract: python TSM_ImageSteganography.py extract <stego_image> <output>")
        print("  Verify: python TSM_ImageSteganography.py verify <stego_image>")
        sys.exit(1)
    
    stego = TSMImageSteganography()
    operation = sys.argv[1].lower()
    
    if operation == 'embed':
        if len(sys.argv) != 5:
            print("Usage: python TSM_ImageSteganography.py embed <image> <client> <output>")
            sys.exit(1)
        
        image_path = sys.argv[2]
        client_path = sys.argv[3]
        output_path = sys.argv[4]
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        if not os.path.exists(client_path):
            print(f"Error: Client file '{client_path}' not found")
            sys.exit(1)
        
        stego.embed_client_in_image(image_path, client_path, output_path)
    
    elif operation == 'extract':
        if len(sys.argv) != 4:
            print("Usage: python TSM_ImageSteganography.py extract <stego_image> <output>")
            sys.exit(1)
        
        stego_image_path = sys.argv[2]
        output_path = sys.argv[3]
        
        if not os.path.exists(stego_image_path):
            print(f"Error: Steganographic image '{stego_image_path}' not found")
            sys.exit(1)
        
        stego.extract_client_from_image(stego_image_path, output_path)
    
    elif operation == 'verify':
        if len(sys.argv) != 3:
            print("Usage: python TSM_ImageSteganography.py verify <stego_image>")
            sys.exit(1)
        
        stego_image_path = sys.argv[2]
        
        if not os.path.exists(stego_image_path):
            print(f"Error: Image file '{stego_image_path}' not found")
            sys.exit(1)
        
        stego.verify_stego_image(stego_image_path)
    
    else:
        print("Invalid operation. Use 'embed', 'extract', or 'verify'")
        sys.exit(1)

if __name__ == "__main__":
    main()
