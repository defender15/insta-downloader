import telebot
from yt_dlp import YoutubeDL
import os

API_TOKEN = '8511268793:AAEgpBhqAzAqJlAiTTft_Eu4iSMMxfAMODE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ Gabi Bot e GATA! Trimite-mi orice link de Instagram (Poză sau Video).")

@bot.message_handler(func=lambda m: True)
def handle_download(message):
    if "instagram.com" in message.text:
        status = bot.reply_to(message, "⏳ Se procesează...")
        try:
            # Setări forțate să accepte orice format
            ydl_opts = {
                'outtmpl': 'file_%(id)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'writethumbnail': True  # Forțează descărcarea imaginii dacă nu e video
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                filename = ydl.prepare_filename(info)

            # Dacă yt-dlp a descărcat doar o miniatură (thumbnail) în loc de video
            if not os.path.exists(filename) and os.path.exists(filename.split('.')[0] + '.jpg'):
                filename = filename.split('.')[0] + '.jpg'

            # Trimitem fișierul bazat pe extensie
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                with open(filename, 'rb') as p:
                    bot.send_photo(message.chat.id, p)
            else:
                with open(filename, 'rb') as v:
                    bot.send_video(message.chat.id, v)
            
            os.remove(filename)
            bot.delete_message(message.chat.id, status.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ Ups! Instagram blochează uneori accesul. Verifică să fie link public.", message.chat.id, status.message_id)
    else:
        bot.reply_to(message, "⚠️ Trimite un link valid.")

bot.infinity_polling()
