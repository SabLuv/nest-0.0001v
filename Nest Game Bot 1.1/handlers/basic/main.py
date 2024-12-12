# БАЗОВЫЕ ИМПОРТЫ
import asyncio

from aiogram import F, Dispatcher, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

from aiogram.enums.dice_emoji import DiceEmoji

import time


# STATE / FSM
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


# ИМПОРТ БАЗЫ ДАННЫХ ИЗ ФАЙЛА DATA.PY
from data import dataBase as db


# ИМПОРТ КЛАВИАТУРЫ ИХ /KEYBOARDS/INLINEKEYBOARDS.PY
import keyboards.basicKeyboard as kb

from config import coder_id
from config import group_log

# ROUTER
router = Router()


#STATE
class SetInfo(StatesGroup):
    name = State()
    
    
    
    
# # ПОЛУЧЕНИЕ НОВОГО ИМЕНИ
# @router.message(SetInfo.name)
# async def set_name(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     await state.update_data(name=message.text)
#     data = await state.get_data()
#     await db.users.update_one({"_id": user_id}, {"$set": {"username": data["name"]}})
#     await message.reply(f"Ваше имя изменено на {data["name"]}")
#     await state.clear()
    
    
        
# СТАРТОВАЯ КОМАНДА
async def str_cmd(message: Message):
    # ВСЕ НЕОБХОДИМОЕ
    user_id = message.from_user.id
    username = message.from_user.full_name
    
    # СОЗДАНИЕ ТАБЛИЦЫ
    pattern = {
        "_id": user_id,
        "gameID": 1,
        "username": username,
        "balance": 5000,
        "rating": 0,
        "bonus": 0,
        "status": "User",
        "isActive": False,
        "numberGame": 0,
        "findSnowman": [0, 0, 0, 0],
        "work_1": False,
        "work_2": False,
        "work_3": False,
    }
    
    # получение базы пользователей из базы
    data = await db.users.find_one({"_id": user_id})
    
    # проверка на регистрацию
    if data:
        await message.reply(f"{username}, ты уже играешь в бота 🤗",
                            reply_markup=await kb.help(message))
    else:
        await db.users.insert_one(pattern)
        await message.answer(f"👋 Привет, {username}\n\n"
                            f"🎁 Я тебе выдал бонус в размере 5000$, ты можешь уже начинать играть и развиваться\n"
                            f"➕ Также можешь добавить меня в чат и играть с друзьями, удачи новичек 😉\n"
                            f"❓ Чтобы узнать команды, нажми на кнопку ниже",
                            reply_markup=await kb.help(message))
        if user_id == coder_id:
            await db.users.update_one({"_id": user_id}, {"$set": {"status": "Coder"}})
    
    
#############
async def balance(msg: Message):
    data = await db.users.find_one({"_id": msg.from_user.id})
    user_id = msg.from_user.id
    
    data = await db.users.find_one({"_id": msg.from_user.id})
    await msg.reply(f"💰 Баланс: <code>{data["balance"]}</code>$",
                            parse_mode="html")
    
#############
async def profile(msg: Message):
    data = await db.users.find_one({"_id": msg.from_user.id})
    user_id = msg.from_user.id
    
    data = await db.users.find_one({"_id": msg.from_user.id})
    await msg.reply(f"👤 Имя: {data["username"]}\n"
                        f"💵 Баланс: <code>{data["balance"]}</code>$\n"
                        f"💎 Статус: <b>{data["status"]}</b>\n",
                        reply_markup=await kb.set_name(msg),
                        parse_mode="html")
    
#############
async def help(msg: Message):
    data = await db.users.find_one({"_id": msg.from_user.id})
    user_id = msg.from_user.id
    
    data = await db.users.find_one({"_id": msg.from_user.id})
    userTAG = msg.from_user.username
    await msg.answer(f"Привет @{userTAG}, я игровой бот None 😎\n\n"
                                            f"Выбери ниже категорию, которая тебе интересна\n"
                                            f"1. 😊 Основное\n2. 🕹️ Игры\n3. 🎁 Кейсы\n4. 🏭 Работа",
                                            reply_markup=await kb.help_category(msg))
    
#############
async def bonus(msg: Message):
    await msg.reply("Чтобы забрать бонус нажми на кнопку ниже",
                            reply_markup=await kb.bonus(msg))
    
#############
async def top(msg: Message):
    cursore = db.users.find().sort("balance", -1).limit(10)
    
    top_list = []
    i = 1
    async for user in cursore:
        player = user["username"]
        balance = user["balance"]
        top_list.append(f"{i}. {player} — 💵{balance}")
        i += 1
    top = "\n".join(top_list)
    await msg.reply(f"Топ 10 лучших игроков бота по балансу:\n{top}")
    
#############
async def send_balance(msg: Message):
    data = await db.users.find_one({"_id": msg.from_user.id})
    user_id = msg.from_user.id
    
    try:    
        r_name = msg.reply_to_message.from_user.username
        r_id = msg.reply_to_message.from_user.id
        # Передать сумму игроку
        if msg.text.lower().startswith('дать'):
            summ = float(msg.text.split()[1])
            if data["balance"] < summ:
                await msg.reply(f"Не хавтает средств для передачи")
            elif data["balance"] >= summ:
                if r_id == user_id:
                    await msg.reply(f"Вы не можете передать деньги самому себе")
                else:
                    await msg.reply(f"Вы передали сумму {summ}$ @{r_name}")
                    await db.users.update_one({"_id": r_id}, {"$inc": {"balance": summ}})
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": -summ}})
    except:
        pass
    
    


    

    

def reg_main(dp: Dispatcher):
    dp.message.register(str_cmd, CommandStart())
    dp.message.register(balance, lambda message: message.text.lower() in ["б", "баланс"])
    dp.message.register(profile, lambda message: message.text.lower() in ["проф", "профиль"])
    dp.message.register(help, lambda message: message.text.lower() == "помощь")
    dp.message.register(bonus, lambda message: message.text.lower() == "бонус")
    dp.message.register(top, lambda message: message.text.lower() == "топ")
    dp.message.register(send_balance, lambda message: message.text.lower().startswith('дать'))