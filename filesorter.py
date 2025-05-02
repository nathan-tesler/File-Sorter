import os
import shutil
import time
from pathlib import Path
from datetime import datetime

DOWNLOADS_PATH = str(Path.home() / "Downloads")
DAYS_UNUSED = 30
DRY_RUN = True

LOG_FILE = os.path.join(DOWNLOADS_PATH, "downloads_cleanup_log.txt")

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

PROTECTED_EXTENSIONS = FILE_TYPES["Scripts"]

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def is_old(file_path, days=DAYS_UNUSED):
    last_access = os.path.getatime(file_path)
    return (time.time() - last_access) > (days * 86400)

def log_action(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}\n"
    print(entry.strip())
    with open(LOG_FILE, "a") as log:
        log.write(entry)

def sort_downloads():
    log_action(f"--- Starting {'Dry Run' if DRY_RUN else 'Actual'} cleanup ---")
    
    for item in os.listdir(DOWNLOADS_PATH):
        item_path = os.path.join(DOWNLOADS_PATH, item)

        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1]
            
            if is_old(item_path) and ext not in PROTECTED_EXTENSIONS:
                if DRY_RUN:
                    log_action(f"[DRY RUN] Would delete: {item_path}")
                else:
                    try:
                        os.remove(item_path)
                        log_action(f"Deleted: {item_path}")
                    except Exception as e:
                        log_action(f"Error deleting {item_path}: {e}")
                continue
            category = get_category(ext)
            dest_folder = os.path.join(DOWNLOADS_PATH, category)
            dest_path = os.path.join(dest_folder, item)

            if DRY_RUN:
                log_action(f"[DRY RUN] Would move: {item_path} → {dest_path}")
            else:
                try:
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(item_path, dest_path)
                    log_action(f"Moved: {item_path} → {dest_path}")
                except Exception as e:
                    log_action(f"Error moving {item_path}: {e}")

    log_action(f"--- Cleanup finished ---")


if __name__ == "__main__":
    sort_downloads()