#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel VNC Integration
Provides remote desktop access capabilities for the TSM system.
"""

import socket
import threading
import time
import base64
import io
import struct
from PIL import Image, ImageGrab
import zlib

class TSMVNCIntegration:
    def __init__(self, server_host='localhost', server_port=5001):
        self.server_host = server_host
        self.server_port = server_port
        self.vnc_socket = None
        self.connected = False
        self.screen_sharing = False
        self.frame_rate = 10  # FPS
        self.quality = 80  # JPEG quality
        self.screen_width = 1920
        self.screen_height = 1080

    def connect_to_vnc_server(self):
        """Connect to VNC server"""
        try:
            self.vnc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.vnc_socket.connect((self.server_host, self.server_port))
            self.connected = True
            print("TSM-SeniorOasisPanel: VNC connection established")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC connection failed: {e}")
            return False

    def disconnect_vnc(self):
        """Disconnect from VNC server"""
        try:
            if self.vnc_socket:
                self.vnc_socket.close()
            self.connected = False
            self.screen_sharing = False
            print("TSM-SeniorOasisPanel: VNC disconnected")
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC disconnect error: {e}")

    def capture_screen(self):
        """Capture current screen"""
        try:
            # Capture screen
            screenshot = ImageGrab.grab()
            
            # Resize if necessary
            if screenshot.size != (self.screen_width, self.screen_height):
                screenshot = screenshot.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
            
            return screenshot
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Screen capture error: {e}")
            return None

    def compress_image(self, image):
        """Compress image for transmission"""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Compress as JPEG
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=self.quality, optimize=True)
            compressed_data = output.getvalue()
            
            # Further compress with zlib
            compressed_data = zlib.compress(compressed_data, 6)
            
            return compressed_data
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Image compression error: {e}")
            return None

    def send_screen_frame(self, image_data):
        """Send screen frame to VNC server"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # Send frame header
            header = struct.pack('>I', len(image_data))  # 4 bytes for data length
            self.vnc_socket.send(header)
            
            # Send compressed image data
            self.vnc_socket.send(image_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Frame send error: {e}")
            return False

    def start_screen_sharing(self):
        """Start screen sharing loop"""
        if not self.connected:
            if not self.connect_to_vnc_server():
                return False
        
        self.screen_sharing = True
        print("TSM-SeniorOasisPanel: Screen sharing started")
        
        # Start screen sharing thread
        sharing_thread = threading.Thread(target=self._screen_sharing_loop, daemon=True)
        sharing_thread.start()
        
        return True

    def _screen_sharing_loop(self):
        """Main screen sharing loop"""
        frame_delay = 1.0 / self.frame_rate
        
        while self.screen_sharing and self.connected:
            try:
                # Capture screen
                screenshot = self.capture_screen()
                if screenshot is None:
                    time.sleep(frame_delay)
                    continue
                
                # Compress image
                compressed_data = self.compress_image(screenshot)
                if compressed_data is None:
                    time.sleep(frame_delay)
                    continue
                
                # Send frame
                if not self.send_screen_frame(compressed_data):
                    break
                
                time.sleep(frame_delay)
                
            except Exception as e:
                print(f"TSM-SeniorOasisPanel: Screen sharing error: {e}")
                time.sleep(frame_delay)

    def stop_screen_sharing(self):
        """Stop screen sharing"""
        self.screen_sharing = False
        print("TSM-SeniorOasisPanel: Screen sharing stopped")

    def send_mouse_event(self, x, y, button, pressed):
        """Send mouse event to VNC server"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # Mouse event format: type(1) + x(2) + y(2) + button(1) + pressed(1)
            event_data = struct.pack('>BHHBB', 1, x, y, button, 1 if pressed else 0)
            self.vnc_socket.send(event_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Mouse event error: {e}")
            return False

    def send_keyboard_event(self, key_code, pressed):
        """Send keyboard event to VNC server"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # Keyboard event format: type(1) + key_code(2) + pressed(1)
            event_data = struct.pack('>BHB', 2, key_code, 1 if pressed else 0)
            self.vnc_socket.send(event_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Keyboard event error: {e}")
            return False

class TSMVNCServer:
    """VNC Server for receiving screen data and input events"""
    
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False

    def start_server(self):
        """Start VNC server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            print(f"TSM-SeniorOasisPanel: VNC Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self._handle_vnc_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"TSM-SeniorOasisPanel: VNC Server error: {e}")
                    break
                    
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC Server error: {e}")
        finally:
            self.stop_server()

    def _handle_vnc_client(self, client_socket, client_address):
        """Handle VNC client connection"""
        client_id = f"{client_address[0]}:{client_address[1]}"
        print(f"TSM-SeniorOasisPanel: VNC Client {client_id} connected")
        
        try:
            while True:
                # Receive frame data
                header = client_socket.recv(4)
                if not header:
                    break
                
                data_length = struct.unpack('>I', header)[0]
                frame_data = b''
                
                while len(frame_data) < data_length:
                    chunk = client_socket.recv(min(4096, data_length - len(frame_data)))
                    if not chunk:
                        break
                    frame_data += chunk
                
                if len(frame_data) == data_length:
                    # Process frame data
                    self._process_frame_data(frame_data, client_id)
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC Client {client_id} error: {e}")
        finally:
            client_socket.close()
            print(f"TSM-SeniorOasisPanel: VNC Client {client_id} disconnected")

    def _process_frame_data(self, frame_data, client_id):
        """Process received frame data"""
        try:
            # Decompress frame data
            decompressed_data = zlib.decompress(frame_data)
            
            # Convert to image
            image = Image.open(io.BytesIO(decompressed_data))
            
            # Save frame (for debugging/monitoring)
            timestamp = int(time.time())
            filename = f"vnc_frame_{client_id}_{timestamp}.jpg"
            image.save(filename)
            
            print(f"TSM-SeniorOasisPanel: Received frame from {client_id}")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Frame processing error: {e}")

    def stop_server(self):
        """Stop VNC server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("TSM-SeniorOasisPanel: VNC Server stopped")

def main():
    """Main function for VNC integration"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server: python TSM_VNCIntegration.py server [host] [port]")
        print("  Client: python TSM_VNCIntegration.py client [host] [port]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'server':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 5001
        
        server = TSMVNCServer(host=host, port=port)
        try:
            server.start_server()
        except KeyboardInterrupt:
            server.stop_server()
    
    elif mode == 'client':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 5001
        
        vnc = TSMVNCIntegration(server_host=host, server_port=port)
        try:
            if vnc.start_screen_sharing():
                print("TSM-SeniorOasisPanel: VNC client running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            vnc.stop_screen_sharing()
            vnc.disconnect_vnc()
    
    else:
        print("Invalid mode. Use 'server' or 'client'")
        sys.exit(1)

if __name__ == "__main__":
    main()
