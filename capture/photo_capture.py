import warnings
from time import sleep
from configparser import SafeConfigParser
from picamera import PiCamera

warnings.filterwarnings('default', category=DeprecationWarning)


def main(config):
        capture_photo(config)


def capture_photo(config):
    with PiCamera() as camera:
        camera = PiCamera(resolution=(1920, 1080), framerate=30)
        camera.iso = (config.get('cam_settings', 'iso'))
        camera.resolution = (config.get('cam_settings', 'resolution'))
        camera.framerate = (config.get('cam_settings', 'framerate'))
        camera.brightness = (config.get('cam_settings', 'brightness'))
        camera.contrast = (config.get('cam_settings', 'contrast'))
        # Camera warm-up time
        sleep(2)
        camera.capture('foo.jpg')


if __name__ == '__main__':
    config = SafeConfigParser()
    config.read('config.ini')
    main(config)
