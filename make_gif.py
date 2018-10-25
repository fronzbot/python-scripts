"""Makes a gif from a series of images."""
import os
import time
import shutil
import imageio

# Edit these variables
IMAGE_DIR = '/share/hass/raw_images'
BACKUP_DIR = '/share/hass/backup'
SAVE_DIR = '/share/hass/gifs'

# In seconds
TARGET_GIF_LENGTH = 5

# Max number of images to use in a GIF
MAX_IMAGES = 48


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

    print("Found {} images".format(len(sortedfiles)))
    # Now check if we even need to bother backing up    
    delete_range = len(sortedfiles) - MAX_IMAGES
    if delete_range > 0:
        for index in range(0, delete_range):
            print("Backing up {}".format(sortedfiles[index]))
            shutil.move(sortedfiles[index], BACKUP_DIR)

    return


def create_new_gif():
    """Use imageio to create a gif."""
    output = os.path.join(SAVE_DIR, 'temp.gif')
    images = []
    files = get_sorted_files()
    framerate = int(len(files) / TARGET_GIF_LENGTH)

    with imageio.get_writer(output, mode='I', fps=framerate) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)

    # And now optimize the gif
    final = os.path.join(SAVE_DIR, 'output.gif')
    if os.path.isfile(final):
        os.remove(final)
    command = "gifsicle -O3 --colors 128 --resize-width 512 {} > {}".format(output, final)
    #command = "convert {} -fuzz 15% -layers Optimize {}".format(output, final)
    os.system(command)
    os.remove(output)

    return


if __name__ == '__main__':
    backup_images()
    create_new_gif()
