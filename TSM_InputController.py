#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Input Controller
نظام التحكم في إدخالات المستخدم وحجبها مؤقتاً
"""

import os
import sys
import time
import threading
import ctypes
from ctypes import wintypes
import win32api
import win32con
import win32gui
import win32process
import win32security
import win32event
import win32service
import win32serviceutil

class TSMInputController:
    """نظام التحكم في إدخالات المستخدم"""
    
    def __init__(self):
        self.input_blocked = False
        self.original_hooks = {}
        self.hook_thread = None
        self.running = False
        
        # رموز Windows API
        self.WH_MOUSE_LL = 14
        self.WH_KEYBOARD_LL = 13
        self.WM_LBUTTONDOWN = 0x0201
        self.WM_LBUTTONUP = 0x0202
        self.WM_RBUTTONDOWN = 0x0204
        self.WM_RBUTTONUP = 0x0205
        self.WM_KEYDOWN = 0x0100
        self.WM_KEYUP = 0x0101
        self.HC_ACTION = 0
        
    def block_all_input(self):
        """حجب جميع إدخالات المستخدم"""
        try:
            if not self.input_blocked:
                # حجب إدخالات الماوس ولوحة المفاتيح
                ctypes.windll.user32.BlockInput(True)
                
                # تثبيت hooks للتحكم الدقيق
                self._install_input_hooks()
                
                self.input_blocked = True
                print("TSM-SeniorOasisPanel: All user input blocked")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Input blocking error: {e}")
            return False
    
    def unblock_all_input(self):
        """إلغاء حجب جميع إدخالات المستخدم"""
        try:
            if self.input_blocked:
                # إلغاء حجب الإدخالات
                ctypes.windll.user32.BlockInput(False)
                
                # إزالة hooks
                self._uninstall_input_hooks()
                
                self.input_blocked = False
                print("TSM-SeniorOasisPanel: All user input unblocked")
                return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Input unblocking error: {e}")
            return False
    
    def _install_input_hooks(self):
        """تثبيت hooks للتحكم في الإدخالات"""
        try:
            # Hook للماوس
            self.mouse_hook = ctypes.windll.user32.SetWindowsHookExW(
                self.WH_MOUSE_LL,
                self._mouse_hook_proc,
                ctypes.windll.kernel32.GetModuleHandleW(None),
                0
            )
            
            # Hook للوحة المفاتيح
            self.keyboard_hook = ctypes.windll.user32.SetWindowsHookExW(
                self.WH_KEYBOARD_LL,
                self._keyboard_hook_proc,
                ctypes.windll.kernel32.GetModuleHandleW(None),
                0
            )
            
            # بدء thread لمعالجة الرسائل
            self.hook_thread = threading.Thread(target=self._hook_message_loop, daemon=True)
            self.hook_thread.start()
            
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Hook installation error: {e}")
    
    def _uninstall_input_hooks(self):
        """إزالة hooks"""
        try:
            if hasattr(self, 'mouse_hook') and self.mouse_hook:
                ctypes.windll.user32.UnhookWindowsHookEx(self.mouse_hook)
            
            if hasattr(self, 'keyboard_hook') and self.keyboard_hook:
                ctypes.windll.user32.UnhookWindowsHookEx(self.keyboard_hook)
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Hook uninstallation error: {e}")
    
    def _mouse_hook_proc(self, nCode, wParam, lParam):
        """معالج hook الماوس"""
        if nCode >= 0 and self.input_blocked:
            # حجب جميع أحداث الماوس
            return 1
        return ctypes.windll.user32.CallNextHookExW(0, nCode, wParam, lParam)
    
    def _keyboard_hook_proc(self, nCode, wParam, lParam):
        """معالج hook لوحة المفاتيح"""
        if nCode >= 0 and self.input_blocked:
            # حجب جميع أحداث لوحة المفاتيح
            return 1
        return ctypes.windll.user32.CallNextHookExW(0, nCode, wParam, lParam)
    
    def _hook_message_loop(self):
        """حلقة معالجة رسائل Windows"""
        try:
            while self.input_blocked:
                # معالجة رسائل Windows
                msg = wintypes.MSG()
                bRet = ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                
                if bRet == 0 or bRet == -1:
                    break
                
                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
                
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Hook message loop error: {e}")
    
    def simulate_mouse_click(self, x, y, button='left'):
        """محاكاة نقرة الماوس"""
        try:
            if not self.input_blocked:
                return False
            
            # تحويل الإحداثيات
            screen_x = int(x * 65535 / 1920)  # تحويل إلى إحداثيات شاشة
            screen_y = int(y * 65535 / 1080)
            
            # محاكاة النقرة
            if button == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
            elif button == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, screen_x, screen_y, 0, 0)
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, screen_x, screen_y, 0, 0)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Mouse simulation error: {e}")
            return False
    
    def simulate_key_press(self, key_code):
        """محاكاة ضغط مفتاح"""
        try:
            if not self.input_blocked:
                return False
            
            # محاكاة الضغط
            win32api.keybd_event(key_code, 0, 0, 0)  # الضغط
            time.sleep(0.01)
            win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)  # الإفلات
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Keyboard simulation error: {e}")
            return False
    
    def simulate_mouse_move(self, x, y):
        """محاكاة حركة الماوس"""
        try:
            if not self.input_blocked:
                return False
            
            # تحويل الإحداثيات
            screen_x = int(x * 65535 / 1920)
            screen_y = int(y * 65535 / 1080)
            
            # محاكاة الحركة
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, 
                               screen_x, screen_y, 0, 0)
            
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Mouse move simulation error: {e}")
            return False

class TSMDesktopController:
    """نظام التحكم في سطح المكتب"""
    
    def __init__(self):
        self.input_controller = TSMInputController()
        self.desktop_handle = None
        
    def get_desktop_handle(self):
        """الحصول على handle سطح المكتب"""
        try:
            self.desktop_handle = win32gui.GetDesktopWindow()
            return self.desktop_handle
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Desktop handle error: {e}")
            return None
    
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
    
    def minimize_all_windows(self):
        """تصغير جميع النوافذ"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for hwnd in windows:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                except:
                    pass
            
            print("TSM-SeniorOasisPanel: All windows minimized")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Window minimize error: {e}")
            return False
    
    def restore_all_windows(self):
        """استعادة جميع النوافذ"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            for hwnd in windows:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                except:
                    pass
            
            print("TSM-SeniorOasisPanel: All windows restored")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Window restore error: {e}")
            return False
    
    def take_full_control(self):
        """السيطرة الكاملة على سطح المكتب"""
        try:
            # حجب جميع الإدخالات
            self.input_controller.block_all_input()
            
            # إخفاء شريط المهام
            self.hide_taskbar()
            
            # تصغير جميع النوافذ
            self.minimize_all_windows()
            
            print("TSM-SeniorOasisPanel: Full desktop control taken")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Full control error: {e}")
            return False
    
    def release_full_control(self):
        """إطلاق السيطرة على سطح المكتب"""
        try:
            # إلغاء حجب الإدخالات
            self.input_controller.unblock_all_input()
            
            # إظهار شريط المهام
            self.show_taskbar()
            
            # استعادة النوافذ
            self.restore_all_windows()
            
            print("TSM-SeniorOasisPanel: Full desktop control released")
            return True
        except Exception as e:
            print(f"TSM-SeniorOasisPanel: Control release error: {e}")
            return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("TSM-SeniorOasisPanel Input Controller Test")
    print("=" * 50)
    
    controller = TSMDesktopController()
    
    try:
        print("TSM-SeniorOasisPanel: Taking full control...")
        controller.take_full_control()
        
        print("TSM-SeniorOasisPanel: Control taken. Press Ctrl+C to release...")
        time.sleep(10)  # انتظار 10 ثواني
        
    except KeyboardInterrupt:
        print("\nTSM-SeniorOasisPanel: Releasing control...")
        controller.release_full_control()
        print("TSM-SeniorOasisPanel: Control released")

if __name__ == "__main__":
    main()
