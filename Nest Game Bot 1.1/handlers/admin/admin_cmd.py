# БАЗОВЫЕ ИМПОРТЫ
import asyncio

from aiogram import F, Router, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

from aiogram.enums.dice_emoji import DiceEmoji

import time



# ИМПОРТ БАЗЫ ДАННЫХ ИЗ ФАЙЛА DATA.PY
from data import dataBase as db


# ИМПОРТ КЛАВИАТУРЫ ИХ /KEYBOARDS/INLINEKEYBOARDS.PY
import keyboards.basicKeyboard as kb

from config import coder_id
from config import group_log

adm_router = Router()

    

async def isCoder(message: Message):
    data = await db.users.find_one({"_id": message.from_user.id})
    user_id = message.from_user.id
    
    if data["status"] == "Coder":
        r_id = message.reply_to_message.from_user.id
        r_name = message.reply_to_message.from_user.full_name
            
                
        
        try:
            r_name = message.reply_to_message.from_user.username
            r_id = message.reply_to_message.from_user.id
            
            # Выдать деньги
            if message.text.startswith('выдать'):
                summ = int(message.text.split()[1])
                await db.users.update_one({"_id": r_id}, {"$inc": {"balance": summ}})
                
                await message.answer(f"Вы выдали пользователю @{r_name}, +{summ}$")
            
            # Обнулить баланс
            if message.text.lower() in "обнулить":
                await db.users.update_one({"_id": r_id}, {"$set": {"balance": 0}})
                
                await message.answer(f"Вы успешно обнулили пользователя @{r_name}")
                
            # Узнать баланс пользователя
            if message.text.lower().startswith('б'):
                user = message.text.split()[1]
                if user == "user":
                    data = await db.users.find_one({"_id": r_id})
                    
                    await message.answer(f"Баланс пользователя @{r_name}\n"
                                        f"Баланс: <code>{data["balance"]}</code>$",
                                        parse_mode="html")
                    
                        
            if message.text.startswith('data'):
                data = await db.users.find_one({"_id": r_id})
                active = message.text.slpit()[1]
                if active == "false":
                    await db.users.update_one({"_id": r_id}, {"$set": {"isActive": False}})
                    await message.reply(f"{data["isActive"]} пользователя изменен на {active}")
                elif active == "true":
                    await db.users.update_one({"_id": r_id}, {"$set": {"isActive": False}})
                    await message.reply(f"{data["isActive"]} пользователя изменен на {active}")
        
        except AttributeError as e:
            pass
            
        
        
        
def reg_admin(dp: Dispatcher):
    dp.message.register(isCoder, lambda message: F.text)