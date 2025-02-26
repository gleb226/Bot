import os

BASE_DIR = os.getcwd()

APP_DIR = os.path.join(BASE_DIR, "app")

DB_DIR = os.path.join(APP_DIR, "databases")

USER_FILES_DIR = os.path.join(BASE_DIR, "user_files")

USERS_DB_PATH = os.path.join(DB_DIR, "users.db")
ERRORS_DB_PATH = os.path.join(DB_DIR, "errors.db")

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(USER_FILES_DIR, exist_ok=True)

folders = {
    "Photos": {
        "path": "photos",
        "subcategories": ["Egypt", "Budapest", "Prague", "School Trips", "Watches", "Diving", "Skiing", "Cat", "Amelia",
                          "Other"]
    },
    "Videos": {
        "path": "videos",
        "subcategories": ["Egypt", "Budapest", "Prague", "School Trips", "Watches", "Diving", "Skiing", "Cat", "Amelia",
                          "Other"]
    },
    "Documents": "documents",
    "Music": "music",
    "Python": "Python Files",
    "Passwords": "passwords",
    "Contacts": "contacts"
}

file_extensions = {
    "Photos": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"],
    "Videos": ["mp4", "mkv", "avi", "mov", "wmv", "flv"],
    "Music": ["mp3", "wav", "flac", "aac", "ogg"],
    "Documents": ["pdf", "docx", "txt", "xlsx", "pptx"],
    "Python": ["py"],
    "Passwords": ["txt", "csv"],
    "Contacts": ["vcf", "txt"]
}

translations = {
    "English": {
        "welcome": "Welcome! Please select a category.",
        "select_subcategory": "Select a subcategory:",
        "send_file": "Please send a {}.",
        "file_too_large": "The file is too large. Please send a smaller file.",
        "file_saved": "{} has been saved successfully!",
        "folder_error": "Invalid folder selected. Please try again."
    }
}

user_selections = {}
