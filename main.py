from pyrogram import Client,filters
import requests
import re
import config 

url = "https://api.safone.me/nsfw"
SPOILER = config.SPOILER_MODE
slangf = 'slang_words.txt'
with open(slangf, 'r') as f:
    slang_words = set(line.strip().lower() for line in f)

Bot = Client(
    "antinude",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

#-----------------------------------------------------------------

@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply("""Hai, yang di sana! Saya adalah bot Penjaga Grup Telegram. Saya di sini untuk membantu Anda menjaga grup Anda tetap bersih dan aman untuk semua orang. Berikut adalah fitur utama yang saya tawarkan:

• **Word Slagging:** Saya dapat mendeteksi dan menghapus pesan bahasa yang tidak pantas di grup Anda.

• **Image Filtering:** Saya juga dapat secara otomatis mendeteksi dan menghapus gambar porno atau NSFW di grup Anda.

Untuk memulai, cukup tambahkan saya ke grup Telegram Anda dan promosikan saya ke admin

Terima kasih telah menggunakan Telegram Group Guardian! Mari jaga grup Anda tetap aman dan terhormat. Powered by @SayaNeko""")

#-----------------------------------------------------------------

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
            if SPOILER:
                await message.reply_photo(x, caption=f"""**WARNING ⚠️** (nude photo)

 **{name}** sent a nude photo

{porn}% porn""", has_spoiler = True)


#-----------------------------------------------------------------

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
                sentence = sentence.replace(word, f'||{word}||')
        if isslang:
            name = message.from_user.first_name
            msgtxt = f"""{name} your message has been deleted due to the presence of inappropriate language. Here is a censored version of your message:
            
{sentence}
            """
            if SPOILER:
                await message.reply(msgtxt)

#--------------------------------------------------------------------------------------------------

Bot.run()
