import asyncio

from aiogram import Bot, Dispatcher

from handlers.basic.main import router
from handlers.basic.callback import callback

from handlers.basic.main import reg_main
from handlers.admin.admin_cmd import reg_admin
from handlers.basic.game import reg_game


from config import TOKEN


def register_dp(dp: Dispatcher) -> None:
    reg_game(dp)
    reg_main(dp)
    reg_admin(dp)
    

bot = Bot(TOKEN)
dp = Dispatcher()

register_dp(dp)




async def main():
    dp.include_routers(router, callback)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot Started")
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    asyncio.run(main())