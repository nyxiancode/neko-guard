from pyrogram import Client, filters
import requests
import re
import config

url = "https://api.safone.me/nsfw"
slangf = 'slang_words.txt'
with open(slangf, 'r') as f:
    slang_words = set(line.strip().lower() for line in f)

Bot = Client(
    "antinude",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply("""Halo! Saya adalah bot Penjaga Grup Telegram. Saya hadir untuk membantu Anda menjaga grup Anda tetap bersih dan aman untuk semua orang. Berikut ini adalah fitur utama yang saya tawarkan:

• **Word Slagging:** Saya dapat mendeteksi dan menghapus pesan dengan bahasa yang tidak pantas di dalam grup Anda.

• **Image Filtering:** Saya juga dapat secara otomatis mendeteksi dan menghapus gambar porno atau NSFW di dalam grup Anda.

Untuk memulai, cukup tambahkan saya ke grup Telegram Anda dan jadikan saya admin.

Terima kasih telah menggunakan Telegram Group Guardian! Mari kita jaga agar grup Anda tetap aman dan tertib. Powered by @SayaNeko""")

@Bot.on_message(filters.group & filters.photo)
async def image(bot, message):
    sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
    isadmin = sender.privileges
    if not isadmin:
        x = await message.download()
        files = {"image": open(x, "rb")}
        roi = requests.post(url, files=files)
        data = roi.json()
        nsfw = data["data"]["is_nsfw"]
        porn = data["data"]["porn"]
        if nsfw:
            name = message.from_user.first_name
            await message.delete()
            await message.reply_photo(x, caption=f"""**PERINGATAN ⚠️** (foto telanjang)

**{name}** telah mengirim foto telanjang

{porn}% pornografi""")

@Bot.on_message(filters.group & filters.text)
async def slang(bot, message):
    sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
    isadmin = sender.privileges
    if not isadmin:
        sentence = message.text
        sent = re.sub(r'\W+', ' ', sentence)
        isslang = False
        for word in sent.split():
            if word.lower() in slang_words:
                isslang = True
                await message.delete()
                break
        if isslang:
            name = message.from_user.first_name
            msgtxt = f"{name}, pesan Anda telah dihapus karena mengandung bahasa yang tidak pantas."
            await message.reply(msgtxt)

Bot.run()
