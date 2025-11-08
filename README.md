# تطبيق طراز - Tiraz Application

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## نظرة عامة - Overview

**طراز** هو تطبيق ويب نموذجي متكامل مبني باستخدام Flask وPython. يوفر التطبيق نظاماً لإدارة العناصر مع إمكانية تصنيفها حسب الأنماط والتصاميم.

**Tiraz** is a complete model web application built with Flask and Python. It provides a comprehensive system for managing items with the ability to categorize them by styles and designs.

## المميزات - Features

- ✨ **إدارة العناصر الكاملة** - Full CRUD operations for items
- 🎨 **تصنيف بالأنماط** - Style-based categorization
- 💾 **قاعدة بيانات SQLite** - SQLite database with SQLAlchemy ORM
- 🌐 **واجهة ثنائية اللغة** - Bilingual interface (Arabic/English)
- 📱 **تصميم متجاوب** - Responsive design
- 🏗️ **معماري MVC** - MVC architecture pattern
- 🔒 **آمن** - Secure with input validation

## الهيكل المعماري - Project Structure

```
Tiraz/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   └── item.py
│   ├── controllers/          # Route controllers
│   │   ├── __init__.py
│   │   ├── main_controller.py
│   │   └── item_controller.py
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── about.html
│   │   └── items/
│   │       ├── list.html
│   │       ├── create.html
│   │       ├── view.html
│   │       └── edit.html
│   └── static/               # Static files
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration settings
├── tests/                    # Test files
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## المتطلبات - Requirements

- Python 3.8 or higher
- pip (Python package manager)

## التثبيت والتشغيل - Installation and Setup

### 1. استنساخ المستودع - Clone the Repository

```bash
git clone https://github.com/OsmanMohamad249/Tiraz.git
cd Tiraz
```

### 2. إنشاء بيئة افتراضية - Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المتطلبات - Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. إعداد المتغيرات البيئية - Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your settings
# Optional: Change SECRET_KEY and DATABASE_URL
```

### 5. تشغيل التطبيق - Run the Application

```bash
python run.py
```

التطبيق سيكون متاحاً على: The application will be available at: `http://localhost:5000`

## الأمان والنشر - Security and Deployment

⚠️ **ملاحظة أمنية مهمة / Important Security Note**:
- التطبيق مُعد للتطوير والتعلم / This application is configured for development and learning
- لا تستخدم `debug=True` في بيئة الإنتاج / Never use `debug=True` in production
- للنشر في الإنتاج، استخدم خادم WSGI مثل Gunicorn أو uWSGI / For production deployment, use a WSGI server like Gunicorn or uWSGI
- غيّر `SECRET_KEY` إلى قيمة سرية قوية / Change `SECRET_KEY` to a strong secret value
- استخدم قاعدة بيانات إنتاجية مثل PostgreSQL أو MySQL / Use a production database like PostgreSQL or MySQL

### نشر الإنتاج - Production Deployment

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

## الاستخدام - Usage

### الصفحة الرئيسية - Home Page
قم بزيارة `http://localhost:5000` لعرض الصفحة الرئيسية
Visit `http://localhost:5000` to see the home page

### إدارة العناصر - Managing Items

1. **عرض العناصر / View Items**: انتقل إلى `/items` لعرض جميع العناصر
2. **إضافة عنصر / Add Item**: انقر على "إضافة عنصر" لإنشاء عنصر جديد
3. **عرض التفاصيل / View Details**: انقر على أي عنصر لعرض تفاصيله
4. **تعديل / Edit**: استخدم زر التعديل لتحديث معلومات العنصر
5. **حذف / Delete**: استخدم زر الحذف لإزالة العنصر

## التقنيات المستخدمة - Technologies Used

### Backend
- **Flask 3.0.0** - Python web framework
- **Flask-SQLAlchemy 3.1.1** - Database ORM
- **SQLite** - Database engine
- **python-dotenv 1.0.0** - Environment variable management

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling
- **JavaScript (ES6+)** - Client-side scripting

## المساهمة - Contributing

المساهمات مرحب بها! يرجى اتباع الخطوات التالية:
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## الترخيص - License

هذا المشروع مرخص تحت رخصة MIT - انظر ملف LICENSE للتفاصيل
This project is licensed under the MIT License - see the LICENSE file for details

## التواصل - Contact

Osman Mohamad - [@OsmanMohamad249](https://github.com/OsmanMohamad249)

رابط المشروع: [https://github.com/OsmanMohamad249/Tiraz](https://github.com/OsmanMohamad249/Tiraz)

---

صُنع بـ ❤️ في السودان | Made with ❤️ in Sudan