from aiogram import types

def main_menu():
    
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    helpBtn = types.KeyboardButton("❓Помощь❓")
    menuBtn = types.KeyboardButton("🍱Меню🍱")
    adminBtn = types.KeyboardButton("👑Администрация👑")
    rkm.row(helpBtn, menuBtn).add(adminBtn)
    return rkm

def help_menu():
    
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contactsBtn = types.KeyboardButton("☎️Контакты☎️")
    locationBtn = types.KeyboardButton("🌇Расположение🌇")
    timetableBtn = types.KeyboardButton("📆Расписание📆")
    backToMainMenu = types.KeyboardButton("🔙Назад в меню🔙")
    rkm.add(contactsBtn, timetableBtn).add(locationBtn).add(backToMainMenu)
    return rkm