import telebot
from yt_dlp import YoutubeDL
import os

API_TOKEN = '8511268793:AAEgpBhqAzAqJlAiTTft_Eu4iSMMxfAMODE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "✅ Botul este activ! Trimite un link public de Instagram.")

@bot.message_handler(func=lambda m: True)
def handle_download(message):
    if "instagram.com" in message.text:
        # Folosim send_message simplu pentru a evita eroarea "message not found"
        status_msg = bot.send_message(message.chat.id, "⏳ Verific link-ul...")
        
        try:
            ydl_opts = {
                'outtmpl': 'file_%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'writethumbnail': True,
                'nocheckcertificate': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                filename = ydl.prepare_filename(info)

            # Verificare extensie poze
            if not os.path.exists(filename):
                for ext in ['.jpg', '.png', '.webp', '.jpeg']:
                    alt_name = os.path.splitext(filename)[0] + ext
                    if os.path.exists(alt_name):
                        filename = alt_name
                        break

            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                with open(filename, 'rb') as p:
                    bot.send_photo(message.chat.id, p)
            else:
                with open(filename, 'rb') as v:
                    bot.send_video(message.chat.id, v)
            
            if os.path.exists(filename):
                os.remove(filename)
            
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Instagram a blocat accesul de pe acest server. Încearcă mai târziu.")
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename)
    else:
        bot.send_message(message.chat.id, "⚠️ Trimite un link de Instagram.")

bot.infinity_polling()
