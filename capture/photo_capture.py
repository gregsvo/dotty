from time import sleep
from picamera import PiCamera, Color
import arrow
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('../config.ini')


def main():

    filename_of_photo = capture_photo()
    file_location_of_photo = upload_photo(filename_of_photo)
    store_photo_info(filename_of_photo, file_location_of_photo)


def capture_photo(config_mode):
    config_mode = config_mode if config_mode else 'CAMERA_PROD'
    time = get_current_time()
    save_location = config.get(config_mode, 'SAVE_LOCATION')
    filename = '{}{}.jpg'.format(save_location, time.timestamp)

    with PiCamera() as camera:
        camera.iso = config.get(config_mode, 'ISO')
        camera.resolution = config.get(config_mode, 'RESOLUTION')
        camera.framerate = config.get(config_mode, 'FRAMERATE')
        sleep(config.get(config_mode, 'SLEEP_TIME_SECS'))
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = config.get(config_mode, 'EXPOSURE_MODE')
        g = camera.awb_gains
        camera.awb_mode = config.get(config_mode, 'AWB_MODE')
        camera.awb_gains = g
        camera.annotate_foreground = Color(config.get(config_mode, 'TIMESTAMP_BACKGROUND'))
        camera.annotate_background = Color(config.get(config_mode, 'TIMESTAMP_FOREGROUND'))
        camera.annotate_text = time.format(config.get(config_mode, 'TIMESTAMP_FORMAT'))
        camera.capture(filename)
        sleep(config.get(config_mode, 'SLEEP_TIME_SECS'))

        return filename


def upload_photo(filename_of_photo):
    return 'file_location_of_photo'


def store_photo_info(filename_of_photo, file_location_of_photo):
    pass


def get_current_time():
    return arrow.utcnow().to(config.get(config_mode,'TIME_ZONE'))


if __name__ == '__main__':
    main()
