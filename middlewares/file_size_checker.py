from aiogram import types, Router

from handlers.error_handler import error_handler
from utils.file_utils import get_user_category, handle_text_file, get_file_info, is_valid_extension, get_folder_path, \
    save_file

file_size_router = Router()

MAX_FILE_SIZE = 200 * 1024 * 1024


@file_size_router.message(lambda message: message.content_type in ["photo", "document", "video", "audio", "text"])
@error_handler("file_handler")
async def handle_file(message: types.Message):
    if message.document and message.document.file_size > MAX_FILE_SIZE:
        await message.answer("The file is too large. Maximum size is 200MB.")
        return

    category, subcategory = get_user_category(message.chat.id)

    if not category:
        await message.answer("Please select a category first.")
        return

    if category in ["Passwords", "Contacts"]:
        await handle_text_file(message, category)
        return

    file_info = await get_file_info(message)
    if not file_info:
        return

    file_id, extension = file_info
    if not is_valid_extension(category, extension):
        await message.answer("Unsupported file format for the selected category.")
        return

    folder_path = get_folder_path(category, subcategory)
    await save_file(message.bot, file_id, folder_path, extension, message.chat.id, category)
