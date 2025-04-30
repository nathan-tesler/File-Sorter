import os
import shutil
from pathlib import Path

DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Define folders and associated extensions
FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg"],
    "Scripts": [".py", ".js", ".sh", ".bat", ".c", ".h", ".json"],
    "Others": []
}

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def sort_downloads():
    for item in os.listdir(DOWNLOADS_PATH):
        item_path = os.path.join(DOWNLOADS_PATH, item)

        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1]
            category = get_category(ext)
            dest_folder = os.path.join(DOWNLOADS_PATH, category)
            os.makedirs(dest_folder, exist_ok=True)

            try:
                shutil.move(item_path, os.path.join(dest_folder, item))
                print(f"Moved: {item} -> {category}/")
            except Exception as e:
                print(f"Error moving {item}: {e}")


if __name__ == "__main__":
    sort_downloads()