from aiogram import types, Dispatcher
from vars_examples import bot
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation
from keyboards import admin_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from databases import databases_controller
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query


id = None

async def check_for_admin(message: types.Message):
    global id
    id = message.from_user.id
    await message.delete()
    try:
        await bot.send_message(message.from_user.id, "Вы прошли проверку на администратора", reply_markup=admin_keyboard.admin_menu())
    except (CantInitiateConversation, BotBlocked):
        await message.answer("Общение с ботом через ЛС\nНапишите ему: @samurai_jp_bot")


class FSMMenuAdding(StatesGroup):
    photo = State()
    name = State()
    descrip = State()
    value = State()
    
    
async def change_menu(message: types.Message):
    await message.reply("Какие изменения в меню вы хотите произвести?", reply_markup=admin_keyboard.change_menu())
    
    
async def change_info(message: types.Message):
    await message.reply("Какую информацию вы хотите изменить?", reply_markup=admin_keyboard.change_info())

    
async def fsm_start(message: types.Message):
    if message.from_user.id == id:
        await FSMMenuAdding.photo.set()
        await message.reply("Загрузите фото блюда, в описании укажите URL на фото", reply_markup=admin_keyboard.cancel_menu())
        
        
async def cancel_fsm(message: types.Message, state: FSMContext):
    if message.from_user.id == id:
        curr_state = state.get_state()
        if curr_state == None:
            return
        await state.finish()
        await message.reply("Добавление отменено", reply_markup=admin_keyboard.admin_menu())
        
        

async def set_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == id:
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id + "$" + message.caption
        await FSMMenuAdding.next()
        await bot.send_message(message.from_user.id, "Введите название")
        
        
async def set_name(message: types.Message, state: FSMContext):
    if message.from_user.id == id:
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMMenuAdding.next()
        await bot.send_message(message.from_user.id, "Ведите описание")
        
        
async def set_descrip(message: types.Message, state: FSMContext):
    if message.from_user.id == id:
        async with state.proxy() as data:
            data["descrip"] = message.text
        await FSMMenuAdding.next()
        await bot.send_message(message.from_user.id, "Укажите цену")
        
        
    
async def set_value(message: types.Message, state: FSMContext):
    if message.from_user.id == id:
        
        async def isdigit_check(message):
            try:
                msg = int(message.text)
                print("price float converted OK")
                return msg
            except ValueError:
                await message.reply("Укажите значение цены в числовом значении")
                await isdigit_check(message)
            
        async with state.proxy() as data:
            print("dictionary 'DATA' opened OK")
            data["value"] = await isdigit_check(message)
            print("dictionary 'DATA' inserted OK")
            await databases_controller.menu_add(data)
        
        await state.finish()
        await bot.send_message(message.from_user.id, "Блюдо добавлено", reply_markup=admin_keyboard.admin_menu())



async def load_for_delete_from_menu(message: types.Message):
    if message.from_user.id == id:
        menu = await databases_controller.load_menu_for_admin()
        for item in menu:
            await bot.send_photo(message.from_user.id, item[0].split()["$"], f"Название: {item[1]}\nОписание: {item[2]}\nСтоимость: {item[3]}")
            ikm = InlineKeyboardMarkup()
            delBtn = InlineKeyboardButton(f"Удалить {item[1]}", callback_data=f"del {item[1]}")
            ikm.add(delBtn)
            await bot.send_message(message.from_user.id, "^^^", reply_markup=ikm)


async def delete_from_menu(callback: types.CallbackQuery):
    name = callback.data.replace("del ", "")
    await databases_controller.del_from_menu(name)
    await callback.answer(f'Блюдо "{name}" удалено', show_alert=True)


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(check_for_admin, lambda x: x.text.startswith("👑Администрация👑"), is_chat_admin=True)
    dp.register_message_handler(change_menu, lambda msg: msg.text.startswith("✏️Изменить меню✏️"))
    dp.register_message_handler(change_info, lambda msg: msg.text.startswith("📄Изменить информацию📄"))
    dp.register_message_handler(fsm_start, lambda msg: msg.text.startswith("➕Добавить в меню➕"))
    dp.register_message_handler(cancel_fsm, lambda msg: msg.text.startswith("❌Отмена❌"), state="*")
    dp.register_message_handler(set_photo, content_types=["photo"], state=FSMMenuAdding.photo)
    dp.register_message_handler(set_name, state=FSMMenuAdding.name)
    dp.register_message_handler(set_descrip, state=FSMMenuAdding.descrip)
    dp.register_message_handler(set_value, state=FSMMenuAdding.value)
    dp.register_message_handler(load_for_delete_from_menu, lambda x: x.text.startswith("❌Удалить из меню❌"))
    dp.register_callback_query_handler(delete_from_menu, lambda cb: cb.data and cb.data.startswith("del "))