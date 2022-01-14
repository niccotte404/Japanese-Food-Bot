from vars_examples import dp, bot
from aiogram import types, Dispatcher
from keyboards import client_keyboard
from package.admin import id
from keyboards.admin_keyboard import admin_menu
from databases import databases_controller
from vars_examples import payment_token
from time import sleep
from aiogram.types.message import ContentType

async def start_bot(message: types.Message):
    await message.answer("Добро пожаловать в Samurai Food", reply_markup=client_keyboard.main_menu())
    
async def for_help_answer(message: types.Message):
    await message.reply("Здесь вы можете заказать еду и просто побеседовать с нашим сообществом)", reply_markup=client_keyboard.help_menu())
    
    
    

async def for_menu_answer(message: types.Message):
    values = await databases_controller.load_menu()
    for item in values:
        url = item[0].split("$")[1]
        price = int(item[3]) * 100
        lblPrice = types.LabeledPrice(label=f"{item[1]}", amount=price)
        await bot.send_invoice(
            message.from_user.id,
            title = f"*{item[1]}*",
            description = f"{item[2]}",
            provider_token=payment_token,
            currency="rub",
            photo_url = f"{url}",
            photo_height=512,
            photo_width=800,
            photo_size=512,
            is_flexible=False,
            prices=[lblPrice],
            need_email=True,
            need_phone_number=True,
            need_shipping_address=True,
            start_parameter="sushi",
            payload=f"Клиент заказал: {item[1]}"
        )
        
        if item != values[-1]:
            sleep(3)
    
    if payment_token.split(":")[1] == "TEST":
        await bot.send_message(message.from_user.id, "*ВНИМАНИЕ ПОДКЛЮЧЕН ТЕСТОВЫЙ ПЛАТЕЖ*\nЧтобы оплатить покупку, воспользуйтесь реквизитами: `1111 1111 1111 1026, 12/22, CVC 000`")


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        
        
        
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(message.chat.id, "*Спасибо за покупку*\nМы рады, что вы выбрали именно наш ресторан! Курьер скоро будет, наслаждайтесь!")


async def for_contacts_answer(message: types.Message):
    await message.reply("Наш телефон: +7**********\nНаша почта: j*******d@mail.ru")
    
async def for_location_answer(message: types.Message):
    await message.reply("Япония, г. Васаби, ул. Лосось, д.25")
    
async def for_timetable_answer(message: types.Message):
    await message.reply("Пн-Пт: 8.00-23.00, Сб-Вс: 9.00-21.00")
    
async def for_backToMenu_answer(message: types.Message):
    await message.reply("Главное меню", reply_markup=client_keyboard.main_menu())


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=["start"])
    dp.register_message_handler(for_help_answer, lambda message: message.text.startswith("❓Помощь❓"))
    dp.register_message_handler(for_menu_answer, lambda message: message.text.startswith("🍱Меню🍱"))
    dp.register_message_handler(for_contacts_answer, lambda message: message.text.startswith("☎️Контакты☎️"))
    dp.register_message_handler(for_location_answer, lambda message: message.text.startswith("🌇Расположение🌇"))
    dp.register_message_handler(for_timetable_answer, lambda message: message.text.startswith("📆Расписание📆"))
    dp.register_message_handler(for_backToMenu_answer, lambda message: message.text.startswith("🔙Назад в меню🔙"))
    dp.register_pre_checkout_query_handler(process_pre_checkout_query, lambda query: True)
    dp.register_message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)