from aiogram import types, Dispatcher

def admin_menu():
    
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    changeTimeTableBtn = types.KeyboardButton("📄Изменить информацию📄")
    addToMenuBtn = types.KeyboardButton("✏️Изменить меню✏️")
    rkm.add(changeTimeTableBtn).add(addToMenuBtn)
    return rkm

def change_info():
    
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    changeTimeTableBtn = types.KeyboardButton("📆Изменить расписание📆")
    changeLocation = types.KeyboardButton("🌇Изменить расположение🌇")
    changeContacts = types.KeyboardButton("☎️Изменить контакты☎️")
    backToAdminMenu = types.KeyboardButton("🔙Назад в меню🔙")
    rkm.add(changeTimeTableBtn, changeLocation).add(changeContacts).add(backToAdminMenu)
    return rkm

def change_menu():
    
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    addToMenu = types.KeyboardButton("➕Добавить в меню➕")
    delFromMenu = types.KeyboardButton("❌Удалить из меню❌")
    backToAdminMenu = types.KeyboardButton("🔙Назад в меню🔙")
    rkm.add(addToMenu, delFromMenu).add(backToAdminMenu)
    return rkm

def cancel_menu():
    
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancelBtn = types.KeyboardButton("❌Отмена❌")
    rkm.add(cancelBtn)
    return rkm