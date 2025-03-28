from aiogram.filters import Command
from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.common.config import translations, folders, user_selections
from app.databases.user_database import db
from app.handlers.error_handler import error_handler

user_router = Router()


@user_router.message(Command("start", "hello", "hi"))
@error_handler("/start")
async def start(message: types.Message):
    buttons = [KeyboardButton(text=category) for category in folders.keys()]
    keyboard = []

    for i in range(0, len(buttons), 2):
        keyboard.append(buttons[i:i + 2])

    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer(translations["English"]["welcome"], reply_markup=markup)
    db.add_user(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name if message.from_user.last_name else "",
        username=message.from_user.username if message.from_user.username else "",
        language_code=message.from_user.language_code if message.from_user.language_code else "unknown",
        is_premium=message.from_user.is_premium if hasattr(message.from_user, 'is_premium') else False,
        chat_id=message.chat.id,
        chat_type=message.chat.type
    )


@user_router.message(lambda message: message.text in folders)
@error_handler("category_selection")
async def category_selection(message: types.Message):
    category = message.text
    user_selections[message.chat.id] = {"category": category, "subcategory": None}

    if isinstance(folders[category], dict) and "subcategories" in folders[category]:
        buttons = [KeyboardButton(text=sub) for sub in folders[category]["subcategories"]]
        keyboard = []

        for i in range(0, len(buttons), 2):
            keyboard.append(buttons[i:i + 2])

        markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        await message.answer(translations["English"]["select_subcategory"], reply_markup=markup)
    else:
        await message.answer(translations["English"]["send_file"].format(category))


@user_router.message(lambda message: any(
    message.text in folders[cat].get("subcategories", []) for cat in folders if isinstance(folders[cat], dict)))
@error_handler("subcategory_selection")
async def handle_subcategory(message: types.Message):
    chat_id = message.chat.id
    category = user_selections.get(chat_id, {}).get("category")
    if not category:
        await message.answer("Please select a category first.")
        return

    user_selections[chat_id]["subcategory"] = message.text
    await message.answer(translations["English"]["send_file"].format(category))
