import telebot
from yt_dlp import YoutubeDL
import os

# Token-ul tau
API_TOKEN = '8511268793:AAEgpBhqAzAqJlAiTTft_Eu4iSMMxfAMODE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ Gabi Bot e gata! Trimite-mi un link de Instagram pentru Video sau Poză.")

@bot.message_handler(func=lambda m: True)
def handle_download(message):
    if "instagram.com" in message.text:
        status = bot.reply_to(message, "⏳ Procesez link-ul...")
        try:
            # Opțiuni pentru a descărca orice (video sau imagine)
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloaded_file.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                filename = ydl.prepare_filename(info)
            
            # Verificăm ce am descărcat și trimitem corespunzător
            if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                with open(filename, 'rb') as p:
                    bot.send_photo(message.chat.id, p)
            else:
                with open(filename, 'rb') as v:
                    bot.send_video(message.chat.id, v)
            
            # Ștergem fișierul după trimitere
            if os.path.exists(filename):
                os.remove(filename)
            bot.delete_message(message.chat.id, status.message_id)

        except Exception as e:
            bot.edit_message_text("❌ Eroare! Link-ul e privat sau invalid. (Doar link-uri publice)", message.chat.id, status.message_id)
            # Curățăm în caz de eroare
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename)
    else:
        bot.reply_to(message, "⚠️ Te rog trimite un link de Instagram.")

bot.infinity_polling()
