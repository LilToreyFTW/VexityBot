#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Server
A TCP file transfer server with multi-client support and VNC integration capabilities.
"""

import socket
import threading
import os
import sys
import time
import logging
from datetime import datetime

class TSMSeniorOasisPanelServer:
    def __init__(self, host='localhost', port=5000, max_clients=10):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.server_files_dir = "server_files"
        self.max_file_size = 100 * 1024 * 1024  # 100MB limit
        self.buffer_size = 1024
        
        # Create server files directory
        self._create_server_directory()
        
        # Setup logging
        self._setup_logging()
        
        # Server socket
        self.server_socket = None
        self.clients = []
        self.running = False

    def _create_server_directory(self):
        """Create server_files directory if it doesn't exist"""
        try:
            if not os.path.exists(self.server_files_dir):
                os.makedirs(self.server_files_dir)
                print(f"TSM-SeniorOasisPanel: Created directory {self.server_files_dir}")
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Error creating directory: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Setup logging for server activity"""
        log_filename = f"tsm_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _sanitize_filename(self, filename):
        """Sanitize filename to prevent directory traversal attacks"""
        # Remove any path separators and dangerous characters
        filename = os.path.basename(filename)
        # Remove any remaining dangerous characters
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        return filename

    def _handle_client(self, client_socket, client_address):
        """Handle individual client connections"""
        client_id = f"{client_address[0]}:{client_address[1]}"
        self.logger.info(f"TSM-SeniorOasisPanel: Client {client_id} connected")
        
        try:
            # Send welcome message
            welcome_msg = "Welcome to TSM-SeniorOasisPanel Server!\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            while True:
                # Receive command from client
                command_data = client_socket.recv(self.buffer_size).decode('utf-8')
                if not command_data:
                    break
                
                command = command_data.strip()
                self.logger.info(f"TSM-SeniorOasisPanel: Received command from {client_id}: {command}")
                
                if command.startswith('UPLOAD'):
                    self._handle_upload(client_socket, command, client_id)
                elif command.startswith('DOWNLOAD'):
                    self._handle_download(client_socket, command, client_id)
                elif command == 'VNC_REQUEST':
                    self._handle_vnc_request(client_socket, client_id)
                elif command == 'EXIT':
                    break
                else:
                    error_msg = "ERROR: Invalid command\n"
                    client_socket.send(error_msg.encode('utf-8'))
                    
        except Exception as e:
            self.logger.error(f"TSM-SeniorOasisPanel: Error handling client {client_id}: {e}")
        finally:
            client_socket.close()
            if client_id in self.clients:
                self.clients.remove(client_id)
            self.logger.info(f"TSM-SeniorOasisPanel: Client {client_id} disconnected")

    def _handle_upload(self, client_socket, command, client_id):
        """Handle file upload from client"""
        try:
            # Parse filename from command
            parts = command.split(' ', 1)
            if len(parts) != 2:
                client_socket.send("ERROR: Invalid upload command format\n".encode('utf-8'))
                return
            
            filename = self._sanitize_filename(parts[1])
            filepath = os.path.join(self.server_files_dir, filename)
            
            # Receive file size
            size_data = client_socket.recv(10).decode('utf-8')
            if not size_data:
                client_socket.send("ERROR: No file size received\n".encode('utf-8'))
                return
            
            file_size = int(size_data.strip())
            
            # Check file size limit
            if file_size > self.max_file_size:
                client_socket.send("ERROR: File too large\n".encode('utf-8'))
                return
            
            # Receive file data
            received_size = 0
            with open(filepath, 'wb') as f:
                while received_size < file_size:
                    data = client_socket.recv(min(self.buffer_size, file_size - received_size))
                    if not data:
                        break
                    f.write(data)
                    received_size += len(data)
            
            if received_size == file_size:
                success_msg = f"OK: File {filename} uploaded successfully\n"
                client_socket.send(success_msg.encode('utf-8'))
                self.logger.info(f"TSM-SeniorOasisPanel: File {filename} uploaded by {client_id}")
            else:
                client_socket.send("ERROR: File upload incomplete\n".encode('utf-8'))
                
        except Exception as e:
            error_msg = f"ERROR: Upload failed - {str(e)}\n"
            client_socket.send(error_msg.encode('utf-8'))
            self.logger.error(f"TSM-SeniorOasisPanel: Upload error for {client_id}: {e}")

    def _handle_download(self, client_socket, command, client_id):
        """Handle file download request from client"""
        try:
            # Parse filename from command
            parts = command.split(' ', 1)
            if len(parts) != 2:
                client_socket.send("ERROR: Invalid download command format\n".encode('utf-8'))
                return
            
            filename = self._sanitize_filename(parts[1])
            filepath = os.path.join(self.server_files_dir, filename)
            
            # Check if file exists
            if not os.path.exists(filepath):
                client_socket.send("ERROR: File not found\n".encode('utf-8'))
                return
            
            # Get file size
            file_size = os.path.getsize(filepath)
            
            # Send file size
            size_msg = f"{file_size:010d}"
            client_socket.send(size_msg.encode('utf-8'))
            
            # Send file data
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(self.buffer_size)
                    if not data:
                        break
                    client_socket.send(data)
            
            self.logger.info(f"TSM-SeniorOasisPanel: File {filename} downloaded by {client_id}")
            
        except Exception as e:
            error_msg = f"ERROR: Download failed - {str(e)}\n"
            client_socket.send(error_msg.encode('utf-8'))
            self.logger.error(f"TSM-SeniorOasisPanel: Download error for {client_id}: {e}")

    def _handle_vnc_request(self, client_socket, client_id):
        """Handle VNC screen sharing request"""
        try:
            # Send VNC configuration
            vnc_config = "VNC_CONFIG: Ready for screen sharing\n"
            client_socket.send(vnc_config.encode('utf-8'))
            self.logger.info(f"TSM-SeniorOasisPanel: VNC request from {client_id}")
        except Exception as e:
            self.logger.error(f"TSM-SeniorOasisPanel: VNC error for {client_id}: {e}")

    def start_server(self):
        """Start the TSM-SeniorOasisPanel server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_clients)
            
            self.running = True
            print(f"TSM-SeniorOasisPanel Server started on {self.host}:{self.port}")
            self.logger.info(f"TSM-SeniorOasisPanel Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    client_id = f"{client_address[0]}:{client_address[1]}"
                    self.clients.append(client_id)
                    
                    # Create thread for each client
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        self.logger.error(f"TSM-SeniorOasisPanel: Socket error: {e}")
                    break
                    
        except Exception as e:
            self.logger.error(f"TSM-SeniorOasisPanel: Server error: {e}")
        finally:
            self.stop_server()

    def stop_server(self):
        """Stop the server gracefully"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("TSM-SeniorOasisPanel Server stopped")
        self.logger.info("TSM-SeniorOasisPanel Server stopped")

def main():
    """Main function to run the server"""
    print("=" * 50)
    print("TSM-SeniorOasisPanel Server")
    print("=" * 50)
    
    # Get server configuration
    host = input("Enter server host (default: localhost): ").strip() or 'localhost'
    port_input = input("Enter server port (default: 5000): ").strip()
    port = int(port_input) if port_input else 5000
    
    # Create and start server
    server = TSMSeniorOasisPanelServer(host=host, port=port)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nTSM-SeniorOasisPanel: Server shutdown requested")
        server.stop_server()
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Fatal error: {e}")
        server.stop_server()

if __name__ == "__main__":
    main()
