"""Makes a gif from a series of images."""
import os
import time
import shutil
import imageio

from pycron import LOGGER

# Edit these variables
BASE_DIR = '/share/hass'
IMAGE_DIR = os.path.join(BASE_DIR, 'raw_images2')
BACKUP_DIR = os.path.join(BASE_DIR, 'backup')
SAVE_DIR = os.path.join(BASE_DIR, 'gifs')

# In seconds
TARGET_GIF_LENGTH = 10

# Max number of images to use in a GIF
MAX_IMAGES = 50 


def get_sorted_files():
    """Return sorted filelist."""
    files = os.listdir(IMAGE_DIR)
    fullfiles = [os.path.join(IMAGE_DIR, name) for name in files]
    sortedfiles = sorted(fullfiles, key=os.path.getmtime)

    return sortedfiles


def backup_images():
    """Backup images when we exceed limit."""
    # sort files based on date
    sortedfiles = get_sorted_files() 

    LOGGER.info("Found {} images".format(len(sortedfiles)))
    # Now check if we even need to bother backing up    
    delete_range = len(sortedfiles) - MAX_IMAGES
    LOGGER.info("Need to delete {} files".format(delete_range))
    if delete_range > 0:
        for index in range(0, delete_range):
            print("Backing up {}".format(sortedfiles[index]))
            shutil.move(sortedfiles[index], BACKUP_DIR)

    return


def create_new_gif():
    """Use imageio to create a gif."""
    LOGGER.info("Creating new gif")
    output = os.path.join(SAVE_DIR, 'temp.gif')
    images = []
    files = get_sorted_files()
    black_frame = os.path.join(BASE_DIR, '01_black.jpg')
    LOGGER.info("Appending three black frames to gif.")
    files.append(black_frame)
    files.append(black_frame)
    files.append(black_frame)
    LOGGER.info("Number of files: %s", len(files))
    framerate = max(1, int(len(files) / TARGET_GIF_LENGTH))
    LOGGER.info("Using framerate of {}".format(framerate))

    with imageio.get_writer(output, mode='I', fps=framerate) as writer:
        for filename in files:
            try:
                image = imageio.imread(filename)
                writer.append_data(image)
            except ValueError as e:
                LOGGER.error(e)

    # And now optimize the gif
    final = os.path.join(SAVE_DIR, 'output.gif')
    if os.path.isfile(final):
        LOGGER.info("Removing {}".format(final))
        os.remove(final)
    command = "gifsicle -O3 --colors 256 --resize-width 512 {} > {}".format(output, final)
    #command = "convert {} -fuzz 15% -layers Optimize {}".format(output, final)
    os.system(command)
    os.remove(output)

    return


if __name__ == '__main__':
    backup_images()
    create_new_gif()
    LOGGER.info("Done.")
