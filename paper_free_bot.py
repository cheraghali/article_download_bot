import requests
import json
import time
import os  # اضافه کردن کتابخانه os

TOKEN = os.getenv("TOKEN")  # توکن را از متغیر محیطی می‌خواند
ID = os.getenv("ID")  # ID را از متغیر محیطی می‌خواند

if not TOKEN or not ID:
    raise ValueError("لطفاً TOKEN و ID را به عنوان متغیر محیطی تنظیم کنید.")

BALE_API_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

# تابع برای دریافت پیام‌ها
def get_updates(offset=None):
    url = BALE_API_URL + "getUpdates"
    params = {"offset": offset, "timeout": 30}
    response = requests.get(url, params=params)
    return response.json()

# تابع برای ارسال پیام
def send_message(chat_id, text, keyboard=None):
    url = BALE_API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if keyboard:
        payload["reply_markup"] = keyboard
    requests.post(url, json=payload)

# تابع برای ایجاد دکمه‌های اصلی بدون دسته‌بندی مقالات
def get_main_keyboard():
    keyboard = {
        "keyboard": [[{"text": "🔍 جستجوی مقاله"}],
                      [{"text": "ℹ️ درباره ربات"}],
                      [{"text": "🔗 اشتراک‌گذاری ربات"}]],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    return json.dumps(keyboard)

# تابع برای دریافت لینک مقاله از Sci-Hub
def get_scihub_link(identifier):
    sci_hub_url = f"https://sci-hub.se/{identifier}"
    return sci_hub_url

# حلقه اصلی ربات
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                
                if "message" not in update:
                    continue
                
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                
                if text == "/start":
                    send_message(chat_id, "سلام! من یک ربات برای دریافت مقالات علمی هستم. \n لطفاً از دکمه‌های زیر استفاده کنید.", get_main_keyboard())
                elif text == "ℹ️ درباره ربات":
                    send_message(chat_id, "📚 این ربات به شما کمک می‌کند که مقالات علمی موردنظر خود را به‌راحتی از Sci-Hub دانلود کنید. \n کافیست DOI یا لینک مقاله را ارسال کنید.")
                elif text == "🔍 جستجوی مقاله":
                    send_message(chat_id, "🔎 لطفاً DOI یا لینک مقاله را ارسال کنید.")
                elif text == "🔗 اشتراک‌گذاری ربات":
                    bot_username = ID  # استفاده از ID از متغیر محیطی
                    send_message(chat_id, f"🔗 برای دعوت دیگران به استفاده از این ربات، لینک زیر را به اشتراک بگذارید:\n{bot_username}")
                elif text:
                    link = get_scihub_link(text)
                    send_message(chat_id, f"🔗 لینک مقاله: {link}")
        
        time.sleep(2)

if __name__ == "__main__":
    main()
