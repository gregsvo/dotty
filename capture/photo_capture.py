import warnings
from time import sleep
from picamera import PiCamera

warnings.filterwarnings('default', category=DeprecationWarning)


def main(config):
        capture_photo(config)

def capture_photo(config):
    with PiCamera() as camera:
        camera = PiCamera(resolution=(1920, 1080), framerate=30)
        camera.iso = 100
        camera.resolution = (1024, 768)
        camera.framerate = 30
        camera.brightness = 30
        camera.contrast = 30
        # Camera warm-up time
        sleep(2)
        camera.capture('foo.jpg')


if __name__ == '__main__':
    main()
