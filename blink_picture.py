"""Uses blinkpy library to take picture with blink camera."""
import json
import time
from blinkpy import blinkpy

CREDENTIALS = '/work/auth.json'
SAVE_DIR = '/share/hass/raw_images2'
CAMERAS = ['Camera1', 'CameraKS']
SAVE_CAMERAS = ['Camera1']


def setup():
    """Initialize."""
    with open(CREDENTIALS) as fh:
        data = json.load(fh)
    
    blink = blinkpy.Blink(username=data['username'], password=data['password'])
    blink.start()
    blink.refresh_rate = 1
    return blink

def save_picture(blink):
    """Take the picture."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    for camera in CAMERAS:        
        blink.cameras[camera].snap_picture()
        time.sleep(10)

    for camera in SAVE_CAMERAS:
        blink.cameras[camera].image_to_file('{}/{}_{}.jpg'.format(SAVE_DIR, camera, timestamp))


if __name__ == '__main__':
    blink = setup()
    save_picture(blink)
