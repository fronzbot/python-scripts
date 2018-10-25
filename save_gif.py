"""Backup a file."""
import os
import time
import shutil

SOURCE_FILE = '/share/hass/gifs/output.gif'
BACKUP_DIR = '/share/hass/gifs/old'

if os.path.isfile(SOURCE_FILE):
    timestamp = time.strftime("%Y_%m_%d")
    newfile = os.path.join(BACKUP_DIR, "blink_{}.gif".format(timestamp))
    shutil.copy(SOURCE_FILE, newfile)

