# БАЗОВЫЕ ИМПОРТЫ
import asyncio

from random import choice

from aiogram import F, Router, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

from aiogram.enums.dice_emoji import DiceEmoji


# ИМПОРТ БАЗЫ ДАННЫХ ИЗ ФАЙЛА DATA.PY
from data import dataBase as db


# ИМПОРТ КЛАВИАТУРЫ ИХ /KEYBOARDS/INLINEKEYBOARDS.PY
import keyboards.basicKeyboard as kb

from config import coder_id
from config import group_log


async def game(message: Message):
    user_id = message.from_user.id
    if message.text.lower().startswith('дартс'):
        data = await db.users.find_one({"_id": user_id})
        bid = int(message.text.split()[1])
        
        if data["isActive"] == True:
            await message.reply("Вы уже играете")
        else:
            if data["balance"] < int(bid):
                await message.reply(f"У вас недостаточно средств")
            else:
                await db.users.update_one({"_id": user_id}, {"$set": {"isActive": True}})
                
                dart = await message.answer_dice(DiceEmoji.DART)
                
                await asyncio.sleep(4)
                
                if dart.dice.value == 1:
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": -bid}})
                    await message.reply(f"Ты проиграл <code>-{bid}</code>$", parse_mode="html")
                    
                    await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
                elif dart.dice.value == 2:
                    win = bid * 1.5
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": win}})
                    await message.reply(f"🙂 Вы выиграли <code>+{win}</code>$", parse_mode="html")
                    
                    await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
                elif dart.dice.value == 3:
                    win = bid * 1.5
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": win}})
                    await message.reply(f"😄 Вы выиграли <code>+{win}</code>$", parse_mode="html")
                    
                    await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
                elif dart.dice.value == 4:
                    win = bid * 1.5
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": win}})
                    await message.reply(f"😎 Вы выиграли <code>+{win}</code>$", parse_mode="html")
                    
                    await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
                elif dart.dice.value == 5:
                    win = bid * 1.5
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": win}})
                    await message.reply(f"😯 Вы выиграли <code>+{win}</code>$", parse_mode="html")
                    
                    await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
                elif dart.dice.value == 6:
                    win = bid * 1.5
                    await db.users.update_one({"_id": user_id}, {"$inc": {"balance": win}})
                    await message.reply(f"🤯 Вы выиграли <code>+{win}</code>$", parse_mode="html")
                    
                    await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
                    
                    
async def dice(msg: Message):
    user_id = msg.from_user.id
    data = await db.users.find_one({"_id": user_id})
    
    number = int(msg.text.split()[1])
    bid = int(msg.text.split()[2])
    
    win_emojis = ["🥳", "😄", "🤩", "🤑"]
    loose_emojis = ["😐", "🥱", "😢", "😤"]
    
    select_win = choice(win_emojis)
    select_loose = choice(loose_emojis)
    
    if data["isActive"] == True:
        await msg.reply("Вы уже играете")
    else:
        if data["balance"] < bid:
            await msg.reply(f"У вас недостаточно средств")
        else:
            await db.users.update_one({"_id": user_id}, {"$set": {"isActive": True}})
            
            dice = await msg.answer_dice(DiceEmoji.DICE)
            
            await asyncio.sleep(5)
            
            if number == dice.dice.value:
                summ = bid * 2
                await msg.reply(f"{select_win} Ты угадал число!\n"
                                f"Твой выигрыш <code>+{summ}</code>$",
                                parse_mode="html")
                await db.users.update_one({"_id": user_id}, {"$inc": {"balance": summ}})
                
                await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
            else:
                await msg.reply(f"{select_loose} Ты проиграл\n"
                                f"<code>-{bid}</code>$",
                                parse_mode="html")
                await db.users.update_one({"_id": user_id}, {"$inc": {"balance": -bid}})
                
                await db.users.update_one({"_id": user_id}, {"$set": {"isActive": False}})
    
    




def reg_game(dp: Dispatcher):
    dp.message.register(game, lambda message: message.text.lower().startswith('дартс'))
    dp.message.register(dice, lambda message: message.text.lower().startswith('дайс'))