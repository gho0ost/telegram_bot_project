طيب ماشي، رح أرسل لك هنا محتوى الملفات نصيًا كامل عشان تقدر تنسخها مباشرة:


---

1. ملف bot.py

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

TOKEN = os.environ.get("5905247562:AAGMRpsJztG1Z_zgSKdM4xEmsDOBhZAPnBo")  # أو حط التوكن مباشرة كـ string
ADMIN_ID = int(os.environ.get("5524258673", "0"))  # ضع هنا الـ user_id تبعك من تلجرام

NAME, LOCATION, PHONE, NOTE, PHOTO = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! رجاءً اكتب اسمك الكامل:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("مكان الإقامة (داخل تركيا):")
    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    await update.message.reply_text("رقم الجوال:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("هل تريد إضافة ملاحظة؟ إذا لا، اكتب 'لا'.")
    return NOTE

async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note = update.message.text
    if note.lower() != "لا":
        context.user_data["note"] = note
    else:
        context.user_data["note"] = "بدون ملاحظة"
    await update.message.reply_text("إذا حابب أرسل صورة، أرسلها الآن أو اكتب 'لا'.")
    return PHOTO

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        context.user_data["photo"] = photo_file.file_id
    else:
        context.user_data["photo"] = None

    msg = (
        f"📩 طلب جديد:\\n"
        f"👤 الاسم: {context.user_data['name']}\\n"
        f"📍 الإقامة: {context.user_data['location']}\\n"
        f"📞 الجوال: {context.user_data['phone']}\\n"
        f"📝 الملاحظة: {context.user_data['note']}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

    if context.user_data["photo"]:
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=context.user_data["photo"])

    await update.message.reply_text("تم إرسال طلبك ✅ شكراً لك.")
    return ConversationHandler.END

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["photo"] = None
    await get_photo(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_note)],
            PHOTO: [
                MessageHandler(filters.PHOTO, get_photo),
                MessageHandler(filters.TEXT & ~filters.COMMAND, skip_photo),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


---

2. ملف requirements.txt

python-telegram-bot==20.3


---

3. ملف Procfile

worker: python bot.py


---

إذا بدك، بساعدك خطوة بخطوة ترفعهم على GitHub وتربطهم بـ Render بعدين.
كيف بدك نبلش؟

