import telebot
from yt_dlp import YoutubeDL
import os

# Token-ul tau
API_TOKEN = '8511268793:AAEgpBhqAzAqJlAiTTft_Eu4iSMMxfAMODE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ Botul tău este pregătit! Trimite-mi orice link public de Instagram.")

@bot.message_handler(func=lambda m: True)
def handle_download(message):
    if "instagram.com" in message.text:
        status = bot.reply_to(message, "⏳ Se procesează...")
        try:
            ydl_opts = {
                'outtmpl': 'file_%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'writethumbnail': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                filename = ydl.prepare_filename(info)

            # Fix pentru extensie (poze)
            if not os.path.exists(filename):
                base = os.path.splitext(filename)[0]
                for ext in ['.jpg', '.png', '.webp', '.jpeg']:
                    if os.path.exists(base + ext):
                        filename = base + ext
                        break

            # Trimitere media
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                with open(filename, 'rb') as p:
                    bot.send_photo(message.chat.id, p)
            else:
                with open(filename, 'rb') as v:
                    bot.send_video(message.chat.id, v)
            
            if os.path.exists(filename):
                os.remove(filename)
            bot.delete_message(message.chat.id, status.message_id)

        except Exception as e:
            bot.edit_message_text("❌ Eroare: Instagram blochează accesul. Încearcă mai târziu.", message.chat.id, status.message_id)
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename)
    else:
        bot.reply_to(message, "⚠️ Trimite un link valid de Instagram.")

bot.infinity_polling()
