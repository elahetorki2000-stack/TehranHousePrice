import sys

print("=" * 50)
print("--- فرآیند تست پیش‌نیازهای پروژه قیمت خانه ---")
print("=" * 50)

# ۱. بررسی نسخه پایتون
python_version = sys.version_info
print(f"[✔] نسخه پایتون شما: {python_version.major}.{python_version.minor}.{python_version.micro}")

print("-" * 50)

# ۲. تست کتابخانه‌های مورد نیاز
required_libraries = {
    "pandas": "پانداز (تحلیل داده)",
    "numpy": "نام‌پای (محاسبات عددی)",
    "sklearn": "سایکت‌لرن (ماشین لرنینگ)",
    "joblib": "جاب‌لیب (ذخیره مدل)",
    "django": "جنگو (وب‌سرویس)",
    "rest_framework": "جنگو رست فریم‌ورک (API)"
}

all_passed = True

for lib_name, lib_desc in required_libraries.items():
    try:
        # استفاده از روش استاندارد داینامیک برای تست کتابخانه‌ها
        imported_lib = __import__(lib_name)
        try:
            version = imported_lib.__version__
        except AttributeError:
            version = "نسخه نامشخص"
        print(f"[✔] کتابخانه '{lib_name}' ({lib_desc}) با موفقیت شناسایی شد. نسخه: {version}")
    except ImportError:
        print(f"[❌] خطا: کتابخانه '{lib_name}' ({lib_desc}) نصب نیست!")
        all_passed = False

print("-" * 50)

if all_passed:
    print("[🎉] عالی شد! تمام ابزارها بدون نقص نصب و فعال هستند و سیستم ۱۰۰٪ آماده است.")
else:
    print("[⚠️] برخی از کتابخانه‌ها به درستی لود نشدند.")
print("=" * 50)