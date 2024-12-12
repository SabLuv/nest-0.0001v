# БАЗОВЫЕ ИМПОРТЫ
import asyncio

from aiogram import F, Router, Dispatcher
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
callback = Router()


#STATE
class SetInfo(StatesGroup):
    name = State()
    
    
# ОБРАБОТЧИКИ CALLBACK
@callback.callback_query(F.data)
async def help(callback: CallbackQuery, state: FSMContext):
    data = await db.users.find_one({"_id": callback.from_user.id})
    user_id = callback.from_user.id
    
    if callback.data.split('-')[0] == str(callback.from_user.id):
        if callback.data.split('-')[1] == "how_to_play":
            data = await db.users.find_one({"_id": callback.from_user.id})
            userTAG = callback.from_user.username
            await callback.answer()
                
            await callback.message.answer(f"Привет @{userTAG}, я игровой бот None 😎\n\n"
                                            f"Выбери ниже категорию, которая тебе интересна\n"
                                            f"1. 😊 Основное\n2. 🕹️ Игры\n3. 🎁 Кейсы\n4. 🏭 Работа",
                                            reply_markup=await kb.help_category(callback))
        ##########
        if callback.data.split('-')[1] == "set_name":
            data = await db.users.find_one({"_id": callback.from_user.id})
            await callback.answer()
            await state.set_state(SetInfo.name)
            await callback.message.reply(f"⚠️ Напиши новое имя")
            
        ##########
        if callback.data.split('-')[1] == "base":
            await callback.answer()
            await callback.message.edit_text(f"<code>Проф</code>, <code>профиль</code> - профиль\n"
                                             f"➖➖➖➖➖➖➖➖➖\n"
                                             f"<code>Б</code>, <code>Баланс</code> - баланс\n"
                                             f"➖➖➖➖➖➖➖➖➖\n"
                                             f"<code>Помощь</code> - помощь в боте\n"
                                             f"➖➖➖➖➖➖➖➖➖\n"
                                             f"<code>Бонус</code> - получить бонус\n"
                                             f"➖➖➖➖➖➖➖➖➖\n"
                                             f"<code>Дать</code> - ответить игроку в чате и написать сумму которую хотите передать",
                                             parse_mode="html",
                                             reply_markup=await kb.back_help_menu(callback))
            
        ##########
        if callback.data.split('-')[1] == "games":
            await callback.answer()
            await callback.message.edit_text(f"🎯 <code>Дартс (сумма)</code> - играть в дартс\n"
                                             f"🎲 <code>Дайс (число) (ставка) </code>\n\n"
                                             f"<blockquote>Игры находятся в бета тесте ⚠️</blockquote>",
                                             parse_mode="html",
                                             reply_markup=await kb.back_help_menu(callback))
            
        ##########
        if callback.data.split('-')[1] == "case":
            await callback.answer()
            await callback.message.edit_text(f"<blockquote>Как купить кейсы ❓</blockquote>\n\n"
                                             f"Кейсы пока недоступны",
                                             parse_mode="html",
                                             reply_markup=await kb.back_help_menu(callback))
            
        ##########
        if callback.data.split('-')[1] == "work":
            await callback.answer()
            await callback.message.edit_text(f"⚙️ Работы недоступны",
                                             parse_mode="html",
                                             reply_markup=await kb.back_help_menu(callback))
            
        ##########
        if callback.data.split('-')[1] == "back_help_menu":
            userTAG = callback.from_user.username
            await callback.answer()
            await callback.message.edit_text(f"Привет @{userTAG}, я игровой бот None 😎\n\n"
                                            f"Выбери ниже категорию, которая тебе интересна\n"
                                            f"1. 😊 Основное\n2. 🕹️ Игры\n3. 🎁 Кейсы\n4. 🏭 Работа",
                                            reply_markup=await kb.help_category(callback))
            
        ##########
        if callback.data.split('-')[1] == "static":
            username = callback.from_user.full_name
            if data["status"] == "Coder":
                users_cursor = db.users.find({})
                users = await users_cursor.to_list(length=None)
                if users:
                    await callback.answer()
                    users_list = "\n".join([f"👤 {username} - {user["_id"]}" for user in users])
                    await callback.message.edit_text(f"Список пользователей:\n\n{users_list}",
                                        reply_markup=await kb.adnim_panel(callback))
                else:
                    await callback.message.reply("Пользователи не найдены.")
                    
        ##########
        if callback.data.split('-')[1] == "claim_bonus":
            await callback.answer()
            now = int(time.time())
            
            if data["bonus"] == 0:
                await callback.message.answer(f"Твой бонус составил <code>1500</code>$", parse_mode="html")
                await db.users.update_one({"_id": user_id}, {"$set": {"bonus": now}})
                await db.users.update_one({"_id": user_id}, {"$inc": {"balance": 1500}})
            else:
                last_claim = data["bonus"]
                cooldown = 10800
                
                if now - last_claim < cooldown:
                    await callback.message.answer(f"🙈 <b>Вы уже получали бонус, приходи через 3 часа</b>", parse_mode="html")
                else:
                    await callback.message.answer(f"Твой бонус составил <code>1500</code>$", parse_mode="html")
                    
                    await db.users.update_one({"_id": user_id}, {"$set": {"bonus": now}})
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": 1500}})
                    
    else:
        return await callback.answer("Не твоя кнопка")