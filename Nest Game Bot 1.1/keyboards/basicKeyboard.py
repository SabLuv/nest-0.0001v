from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import Message, CallbackQuery

async def help(message: Message):
    user_id = message.from_user.id
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💫 Помощь", switch_inline_query_current_chat=f"Помощь")]
        ]
    )

async def set_name(message: Message):
    user_id = message.from_user.id
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Изменить имя", callback_data=f"{user_id}-set_name")]
        ]
    )
    
async def back_help_menu(message: Message):
    user_id = message.from_user.id
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data=f"{user_id}-back_help_menu")]
        ]
    )

##########################
help_button = [
    "😊 Основное", 
    "🕹️ Игры", 
    "🎁 Кейсы", 
    "🏭 Работа"
]

callback_help = [
    "base",
    "games",
    "case",
    "work"
]

async def help_category(message: Message):
    user_id = message.from_user.id
    keyboard = InlineKeyboardBuilder()
    for i, j in zip(help_button, callback_help):
        keyboard.add(InlineKeyboardButton(text=i, callback_data=f"{user_id}-{j}"))
    return keyboard.adjust(2).as_markup()


async def bonus(message: Message):
    user_id = message.from_user.id
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎁 Получить бонус", callback_data=f"{user_id}-claim_bonus")]
        ]
    )
    
