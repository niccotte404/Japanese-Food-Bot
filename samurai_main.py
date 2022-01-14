from aiogram.utils import executor
from vars_examples import dp
from package import admin, client, other
from databases import databases_controller

async def beginning(_):
    print("Bot started")
    databases_controller.connecting()
    
client.register_client_handlers(dp)
admin.register_admin_handlers(dp)
other.register_other_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=beginning)