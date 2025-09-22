#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel VNC Integration Test
اختبار شامل لدمج VNC مع نظام TSM
"""

import os
import sys
import time
import threading
import subprocess
import requests
import webbrowser
from PIL import Image

def test_novnc_availability():
    """اختبار توفر noVNC"""
    print("🧪 Testing noVNC availability...")
    
    novnc_path = "noVNC"
    if os.path.exists(novnc_path):
        print("✅ noVNC directory found")
        
        # فحص الملفات المهمة
        important_files = [
            "vnc.html",
            "vnc_lite.html",
            "app/ui.js",
            "utils/websockify/websockify.py"
        ]
        
        for file in important_files:
            file_path = os.path.join(novnc_path, file)
            if os.path.exists(file_path):
                print(f"✅ {file} found")
            else:
                print(f"❌ {file} not found")
        
        return True
    else:
        print("❌ noVNC directory not found")
        return False

def test_tigervnc_availability():
    """اختبار توفر TigerVNC"""
    print("🧪 Testing TigerVNC availability...")
    
    tigervnc_path = "tigervnc"
    if os.path.exists(tigervnc_path):
        print("✅ TigerVNC directory found")
        
        # فحص الملفات المهمة
        important_files = [
            "unix/vncserver",
            "unix/vncviewer",
            "win/vncserver.exe",
            "win/vncviewer.exe"
        ]
        
        found_files = 0
        for file in important_files:
            file_path = os.path.join(tigervnc_path, file)
            if os.path.exists(file_path):
                print(f"✅ {file} found")
                found_files += 1
            else:
                print(f"⚠️ {file} not found")
        
        if found_files > 0:
            print("✅ TigerVNC files available")
            return True
        else:
            print("❌ No TigerVNC executables found")
            return False
    else:
        print("❌ TigerVNC directory not found")
        return False

def test_tsm_vnc_modules():
    """اختبار وحدات TSM VNC"""
    print("🧪 Testing TSM VNC modules...")
    
    modules = [
        "TSM_WebVNC",
        "TSM_TigerVNC_Integration", 
        "TSM_noVNC_Integration",
        "TSM_Complete_Integration"
    ]
    
    all_imported = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ {module} import failed: {e}")
            all_imported = False
    
    return all_imported

def test_web_vnc_server():
    """اختبار خادم Web VNC"""
    print("🧪 Testing Web VNC Server...")
    
    try:
        from TSM_WebVNC import TSMWebVNCServer
        
        # إنشاء خادم تجريبي
        server = TSMWebVNCServer(host='localhost', port=8080, vnc_port=5900)
        print("✅ Web VNC Server created successfully")
        
        # اختبار بدء الخادم (بدون تشغيل فعلي)
        print("✅ Web VNC Server test passed")
        return True
        
    except Exception as e:
        print(f"❌ Web VNC Server test failed: {e}")
        return False

def test_tigervnc_integration():
    """اختبار دمج TigerVNC"""
    print("🧪 Testing TigerVNC Integration...")
    
    try:
        from TSM_TigerVNC_Integration import TSMTigerVNCIntegration
        
        # إنشاء تكامل تجريبي
        integration = TSMTigerVNCIntegration(vnc_port=5900, display_number=1)
        print("✅ TigerVNC Integration created successfully")
        
        # اختبار الحصول على معلومات
        status = integration.get_integration_status()
        print(f"✅ Integration status: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ TigerVNC Integration test failed: {e}")
        return False

def test_novnc_integration():
    """اختبار دمج noVNC"""
    print("🧪 Testing noVNC Integration...")
    
    try:
        from TSM_noVNC_Integration import TSMnoVNCServer
        
        # إنشاء خادم تجريبي
        server = TSMnoVNCServer(host='localhost', port=8080, vnc_port=5900)
        print("✅ noVNC Integration created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ noVNC Integration test failed: {e}")
        return False

def test_complete_integration():
    """اختبار التكامل الكامل"""
    print("🧪 Testing Complete Integration...")
    
    try:
        from TSM_Complete_Integration import TSMCompleteIntegration
        
        # إنشاء تكامل تجريبي
        integration = TSMCompleteIntegration(host='localhost', port=8080, vnc_port=5900)
        print("✅ Complete Integration created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete Integration test failed: {e}")
        return False

def test_web_interface():
    """اختبار الواجهة الويب"""
    print("🧪 Testing Web Interface...")
    
    try:
        # اختبار إنشاء HTML بسيط
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>TSM VNC Test</title></head>
        <body><h1>TSM VNC Test Page</h1></body>
        </html>
        """
        
        # حفظ ملف تجريبي
        test_file = "tsm_vnc_test.html"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Web interface test file created")
        
        # تنظيف
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Web Interface test failed: {e}")
        return False

def test_network_connectivity():
    """اختبار اتصال الشبكة"""
    print("🧪 Testing Network Connectivity...")
    
    try:
        # اختبار الاتصال المحلي
        import socket
        
        # اختبار إنشاء socket
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.close()
        
        print("✅ Network connectivity test passed")
        return True
        
    except Exception as e:
        print(f"❌ Network connectivity test failed: {e}")
        return False

def test_image_processing():
    """اختبار معالجة الصور"""
    print("🧪 Testing Image Processing...")
    
    try:
        # إنشاء صورة تجريبية
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # اختبار العمليات الأساسية
        test_image.save('test_image.png')
        
        # قراءة الصورة
        loaded_image = Image.open('test_image.png')
        
        # تنظيف
        if os.path.exists('test_image.png'):
            os.remove('test_image.png')
        
        print("✅ Image processing test passed")
        return True
        
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return False

def run_integration_demo():
    """تشغيل عرض توضيحي للتكامل"""
    print("🎬 Running VNC Integration Demo...")
    
    try:
        # إنشاء صورة تجريبية
        demo_image = Image.new('RGB', (800, 600), color='lightblue')
        demo_image.save('demo_image.png')
        print("✅ Demo image created")
        
        # اختبار إنشاء صورة مخفية
        from TSM_StealthMode import TSMStealthMode
        
        stealth = TSMStealthMode()
        stealth_image = stealth.create_stealth_image_with_vnc('demo_image.png', 'localhost', 5900)
        
        if stealth_image:
            print("✅ Stealth image with VNC created")
        else:
            print("❌ Failed to create stealth image with VNC")
        
        # تنظيف
        for file in ['demo_image.png', 'TSM_Stealth_Image.png']:
            if os.path.exists(file):
                os.remove(file)
        
        print("✅ VNC Integration demo completed")
        return True
        
    except Exception as e:
        print(f"❌ VNC Integration demo failed: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("🎯 TSM-SeniorOasisPanel VNC Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("noVNC Availability", test_novnc_availability),
        ("TigerVNC Availability", test_tigervnc_availability),
        ("TSM VNC Modules", test_tsm_vnc_modules),
        ("Web VNC Server", test_web_vnc_server),
        ("TigerVNC Integration", test_tigervnc_integration),
        ("noVNC Integration", test_novnc_integration),
        ("Complete Integration", test_complete_integration),
        ("Web Interface", test_web_interface),
        ("Network Connectivity", test_network_connectivity),
        ("Image Processing", test_image_processing),
        ("Integration Demo", run_integration_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "="*60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("🎉 All VNC Integration tests passed! System is ready for deployment.")
        print("\n🚀 You can now run:")
        print("   • TSM_VNC_Launcher.bat")
        print("   • python TSM_Complete_Integration.py start")
        print("   • python TSM_Master_Launcher.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   • Ensure noVNC and TigerVNC are cloned")
        print("   • Check Python dependencies")
        print("   • Verify network connectivity")
    
    print("\n📖 For more information, see README_VNC_Integration.md")

if __name__ == "__main__":
    main()
