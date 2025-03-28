import glob
import os

from aiogram import types, Bot

from app.common.config import folders, translations, user_selections, file_extensions, USER_FILES_DIR


async def save_user_file(file, category, filename):
    category_path = os.path.join(USER_FILES_DIR, category)
    os.makedirs(category_path, exist_ok=True)

    file_path = os.path.join(category_path, filename)
    await file.download(destination_file=file_path)

    return file_path


def get_user_category(chat_id):
    user_data = user_selections.get(chat_id, {})
    return user_data.get("category"), user_data.get("subcategory")


async def handle_text_file(message: types.Message, category: str):
    if message.content_type == "text":
        text_data = message.text
    elif message.content_type == "document":
        file_info = await message.bot.get_file(message.document.file_id)
        downloaded_file = await message.bot.download_file(file_info.file_path)
        text_data = downloaded_file.read().decode('utf-8')
    else:
        await message.answer("Please send text or a text document for this category.")
        return

    category_path = os.path.join(USER_FILES_DIR, category)
    os.makedirs(category_path, exist_ok=True)

    file_path = os.path.join(category_path, f"{category}.txt")

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(text_data + "\n")

    await message.answer(translations["English"]["file_saved"].format(category.capitalize()))


async def get_file_info(message: types.Message):
    if message.content_type == "photo":
        return message.photo[-1].file_id, "jpg"
    elif message.content_type == "video":
        return message.video.file_id, "mp4"
    elif message.content_type == "document":
        return message.document.file_id, message.document.file_name.split('.')[-1].lower()
    elif message.content_type == "audio":
        return message.audio.file_id, "mp3"
    return None, None


def is_valid_extension(category, extension):
    return extension in file_extensions.get(category, [])


def get_folder_path(category, subcategory):
    category_path = os.path.join(USER_FILES_DIR, folders[category]["path"]) if isinstance(folders[category],
                                                                                          dict) else os.path.join(
        USER_FILES_DIR, folders[category])
    return os.path.join(category_path, subcategory) if subcategory else category_path


async def save_file(bot: Bot, file_id: str, folder_path: str, extension: str, chat_id: int, category: str):
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{file_id}.{extension}"
    file_path = os.path.join(folder_path, filename)

    file_info = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file.getbuffer())

    await bot.send_message(chat_id, translations["English"]["file_saved"].format(category.capitalize()))


'''

async def send_files_from_folder(message: types.Message, folder_path: str, file_type: str):
    try:
        files = glob.glob(os.path.join(folder_path, "*"), recursive=True)
        if files:
            for file_path in files:
                with open(file_path, 'rb') as file:
                    await message.answer_document(file)
            await message.answer(f'All files from {file_type.replace("_", " ").capitalize()} have been sent.')
        else:
            await message.answer(f'No files found in the folder for {file_type}.')
    except Exception as e:
        await message.answer(f'Error sending {file_type}: {str(e)}')


'''
