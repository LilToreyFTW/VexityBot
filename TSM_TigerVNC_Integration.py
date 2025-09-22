#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel TigerVNC Integration
دمج TigerVNC مع نظام TSM للتحكم المتقدم
"""

import os
import sys
import time
import threading
import subprocess
import socket
import struct
import json
import tempfile
import shutil
from PIL import Image, ImageGrab
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process

class TSMTigerVNCManager:
    """مدير TigerVNC لـ TSM"""
    
    def __init__(self, vnc_port=5900, display_number=1):
        self.vnc_port = vnc_port
        self.display_number = display_number
        self.tigervnc_path = None
        self.vnc_process = None
        self.running = False
        self.setup_tigervnc()
        
    def setup_tigervnc(self):
        """إعداد TigerVNC"""
        try:
            # البحث عن TigerVNC في المجلد المستنسخ
            tigervnc_dir = 'tigervnc'
            if os.path.exists(tigervnc_dir):
                # البحث عن الملفات التنفيذية
                possible_paths = [
                    os.path.join(tigervnc_dir, 'unix', 'vncserver'),
                    os.path.join(tigervnc_dir, 'unix', 'vncviewer'),
                    os.path.join(tigervnc_dir, 'win', 'vncserver.exe'),
                    os.path.join(tigervnc_dir, 'win', 'vncviewer.exe')
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        self.tigervnc_path = path
                        print(f"TSM-SeniorOasisPanel: TigerVNC found at {path}")
                        break
                
                if not self.tigervnc_path:
                    print("TSM-SeniorOasisPanel: TigerVNC executable not found")
                    self.create_tigervnc_wrapper()
            else:
                print("TSM-SeniorOasisPanel: TigerVNC directory not found")
                self.create_tigervnc_wrapper()
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC setup error: {e}")
            self.create_tigervnc_wrapper()
    
    def create_tigervnc_wrapper(self):
        """إنشاء wrapper لـ TigerVNC"""
        try:
            # إنشاء wrapper script لـ TigerVNC
            wrapper_code = '''#!/usr/bin/env python3
"""
TSM TigerVNC Wrapper
"""

import os
import sys
import subprocess
import socket
import threading
import time

class TSMTigerVNCWrapper:
    def __init__(self, port=5900, display=1):
        self.port = port
        self.display = display
        self.running = False
        
    def start_vnc_server(self):
        """بدء خادم VNC"""
        try:
            # إنشاء خادم VNC بسيط
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', self.port))
            server_socket.listen(5)
            
            self.running = True
            print(f"TSM-SeniorOasisPanel: TigerVNC Wrapper started on port {self.port}")
            
            while self.running:
                try:
                    client_socket, address = server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_vnc_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except:
                    break
                    
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Wrapper error: {e}")
    
    def handle_vnc_client(self, client_socket, address):
        """معالجة عميل VNC"""
        try:
            print(f"TSM-SeniorOasisPanel: VNC Client connected from {address}")
            
            # إرسال معلومات VNC
            vnc_info = {
                'version': 'RFB 003.008',
                'width': 1920,
                'height': 1080,
                'bpp': 32
            }
            
            client_socket.send(json.dumps(vnc_info).encode('utf-8'))
            
            # معالجة طلبات VNC
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    # معالجة طلب VNC
                    self.process_vnc_request(client_socket, data)
                    
                except:
                    break
                    
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC Client handler error: {e}")
        finally:
            client_socket.close()
    
    def process_vnc_request(self, client_socket, data):
        """معالجة طلب VNC"""
        try:
            # معالجة طلبات VNC الأساسية
            if data.startswith(b'RFB'):
                # إرسال استجابة VNC
                response = b'RFB 003.008\\n'
                client_socket.send(response)
            else:
                # معالجة طلبات أخرى
                pass
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC request processing error: {e}")

if __name__ == "__main__":
    wrapper = TSMTigerVNCWrapper()
    wrapper.start_vnc_server()
'''
            
            # حفظ wrapper
            wrapper_file = 'TSM_TigerVNC_Wrapper.py'
            with open(wrapper_file, 'w', encoding='utf-8') as f:
                f.write(wrapper_code)
            
            self.tigervnc_path = wrapper_file
            print("TSM-SeniorOasisPanel: TigerVNC Wrapper created")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Wrapper creation error: {e}")
    
    def start_vnc_server(self):
        """بدء خادم TigerVNC"""
        try:
            if self.tigervnc_path:
                if self.tigervnc_path.endswith('.py'):
                    # تشغيل wrapper
                    self.vnc_process = subprocess.Popen([
                        sys.executable, self.tigervnc_path
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    # تشغيل TigerVNC الأصلي
                    cmd = [self.tigervnc_path, f':{self.display_number}', '-localhost', 'no']
                    self.vnc_process = subprocess.Popen(cmd)
                
                self.running = True
                print(f"TSM-SeniorOasisPanel: TigerVNC Server started on port {self.vnc_port}")
                return True
            else:
                print("TSM-SeniorOasisPanel: TigerVNC path not set")
                return False
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Server start error: {e}")
            return False
    
    def stop_vnc_server(self):
        """إيقاف خادم TigerVNC"""
        try:
            if self.vnc_process:
                self.vnc_process.terminate()
                self.vnc_process.wait(timeout=5)
            
            self.running = False
            print("TSM-SeniorOasisPanel: TigerVNC Server stopped")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Server stop error: {e}")
    
    def get_vnc_info(self):
        """الحصول على معلومات VNC"""
        return {
            'port': self.vnc_port,
            'display': self.display_number,
            'running': self.running,
            'path': self.tigervnc_path
        }

class TSMTigerVNCClient:
    """عميل TigerVNC لـ TSM"""
    
    def __init__(self, server_host='localhost', server_port=5900):
        self.server_host = server_host
        self.server_port = server_port
        self.connected = False
        self.vnc_socket = None
        
    def connect(self):
        """الاتصال بخادم TigerVNC"""
        try:
            self.vnc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.vnc_socket.connect((self.server_host, self.server_port))
            self.connected = True
            
            print(f"TSM-SeniorOasisPanel: TigerVNC Client connected to {self.server_host}:{self.server_port}")
            return True
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Client connection error: {e}")
            return False
    
    def disconnect(self):
        """قطع الاتصال"""
        try:
            if self.vnc_socket:
                self.vnc_socket.close()
            self.connected = False
            print("TSM-SeniorOasisPanel: TigerVNC Client disconnected")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Client disconnect error: {e}")
    
    def send_vnc_command(self, command):
        """إرسال أمر VNC"""
        try:
            if self.connected and self.vnc_socket:
                self.vnc_socket.send(command.encode('utf-8'))
                return True
            else:
                print("TSM-SeniorOasisPanel: Not connected to VNC server")
                return False
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC command send error: {e}")
            return False
    
    def receive_vnc_data(self):
        """استقبال بيانات VNC"""
        try:
            if self.connected and self.vnc_socket:
                data = self.vnc_socket.recv(1024)
                return data
            else:
                return None
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC data receive error: {e}")
            return None

class TSMTigerVNCIntegration:
    """دمج TigerVNC مع TSM"""
    
    def __init__(self, vnc_port=5900, display_number=1):
        self.vnc_manager = TSMTigerVNCManager(vnc_port, display_number)
        self.vnc_client = None
        self.integration_active = False
        
    def start_integration(self):
        """بدء دمج TigerVNC"""
        try:
            # بدء خادم TigerVNC
            if self.vnc_manager.start_vnc_server():
                time.sleep(2)  # انتظار بدء الخادم
                
                # إنشاء عميل VNC
                self.vnc_client = TSMTigerVNCClient(
                    server_host='localhost',
                    server_port=self.vnc_manager.vnc_port
                )
                
                # الاتصال بالخادم
                if self.vnc_client.connect():
                    self.integration_active = True
                    print("TSM-SeniorOasisPanel: TigerVNC Integration started successfully")
                    return True
                else:
                    print("TSM-SeniorOasisPanel: Failed to connect TigerVNC client")
                    return False
            else:
                print("TSM-SeniorOasisPanel: Failed to start TigerVNC server")
                return False
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Integration start error: {e}")
            return False
    
    def stop_integration(self):
        """إيقاف دمج TigerVNC"""
        try:
            if self.vnc_client:
                self.vnc_client.disconnect()
            
            if self.vnc_manager:
                self.vnc_manager.stop_vnc_server()
            
            self.integration_active = False
            print("TSM-SeniorOasisPanel: TigerVNC Integration stopped")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: TigerVNC Integration stop error: {e}")
    
    def get_integration_status(self):
        """الحصول على حالة الدمج"""
        return {
            'active': self.integration_active,
            'vnc_info': self.vnc_manager.get_vnc_info() if self.vnc_manager else None,
            'client_connected': self.vnc_client.connected if self.vnc_client else False
        }
    
    def send_screen_data(self, screen_data):
        """إرسال بيانات الشاشة عبر TigerVNC"""
        try:
            if self.integration_active and self.vnc_client:
                # تحويل بيانات الشاشة إلى تنسيق VNC
                vnc_data = self.convert_to_vnc_format(screen_data)
                
                # إرسال البيانات
                return self.vnc_client.send_vnc_command(vnc_data)
            else:
                print("TSM-SeniorOasisPanel: TigerVNC Integration not active")
                return False
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Screen data send error: {e}")
            return False
    
    def convert_to_vnc_format(self, screen_data):
        """تحويل بيانات الشاشة إلى تنسيق VNC"""
        try:
            # تحويل بيانات الشاشة إلى تنسيق VNC
            if isinstance(screen_data, Image.Image):
                # تحويل الصورة إلى بيانات VNC
                vnc_data = {
                    'type': 'screen_update',
                    'width': screen_data.width,
                    'height': screen_data.height,
                    'data': screen_data.tobytes()
                }
                return json.dumps(vnc_data)
            else:
                return str(screen_data)
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC format conversion error: {e}")
            return None

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server: python TSM_TigerVNC_Integration.py server [port] [display]")
        print("  Client: python TSM_TigerVNC_Integration.py client [host] [port]")
        print("  Integration: python TSM_TigerVNC_Integration.py integration [port] [display]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'server':
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 5900
        display = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        
        manager = TSMTigerVNCManager(port, display)
        try:
            if manager.start_vnc_server():
                print("TSM-SeniorOasisPanel: TigerVNC Server running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_vnc_server()
    
    elif mode == 'client':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 5900
        
        client = TSMTigerVNCClient(host, port)
        try:
            if client.connect():
                print("TSM-SeniorOasisPanel: TigerVNC Client connected. Press Ctrl+C to disconnect.")
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            client.disconnect()
    
    elif mode == 'integration':
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 5900
        display = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        
        integration = TSMTigerVNCIntegration(port, display)
        try:
            if integration.start_integration():
                print("TSM-SeniorOasisPanel: TigerVNC Integration running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            integration.stop_integration()
    
    else:
        print("Invalid mode. Use 'server', 'client', or 'integration'")
        sys.exit(1)

if __name__ == "__main__":
    main()
