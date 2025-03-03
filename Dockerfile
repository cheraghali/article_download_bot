# استفاده از ایمیج پایه پایتون
FROM python:3.9-slim

# تنظیم دایرکتوری کار درون کانتینر
WORKDIR /app

# کپی کردن فایل‌های پروژه به دایرکتوری کار
COPY . .

# نصب وابستگی‌های لازم
RUN pip install --no-cache-dir -r requirements.txt

# دستور اجرای برنامه
CMD ["python", "paper_free_bot.py"]