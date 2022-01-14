import json, string
from aiogram import types, Dispatcher


async def stopwords_filter(message: types.Message):
    stw = json.load(open("stopwords.json"))
    for i in message.text.split(" "):
        item = i.lower().translate(str.maketrans("", "", string.punctuation))
        if item in stw:
            await message.reply("В вашем сообщении выявлены запрещенные слова")
            await message.delete()
    

def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(stopwords_filter)