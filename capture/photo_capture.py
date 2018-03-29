from time import sleep
from picamera import PiCamera
import arrow


def main():
    filename_of_photo = capture_photo()
    file_location_of_photo = upload_photo(filename_of_photo)
    store_photo_info(filename_of_photo, file_location_of_photo)


def capture_photo():
    time = get_current_time()
    save_location = '/home/pi/Pictures/'
    filename = '{}{}.jpg'.format(save_location, time.timestamp)
    with PiCamera() as camera:
        camera.iso = 100
        camera.resolution = (1024, 768)
        camera.framerate = 30
        sleep(2)
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        camera.annotate_foreground = Color('black')
        camera.annotate_background = Color('white')
        camera.annotate_text = time.format('MM/DD/YYYY : hh:mm a')
        camera.capture(filename)
        sleep(2)
        return filename


def upload_photo(filename_of_photo):
    return 'file_location_of_photo'


def store_photo_info(filename_of_photo, file_location_of_photo):
    pass


def get_current_time():
    return arrow.utcnow().to('US/Eastern')


if __name__ == '__main__':
    main()
