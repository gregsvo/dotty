from io import BytesIO
from picamera import PiCamera, Color
from time import sleep
import arrow
import boto3
from configparser import ConfigParser
import os

config = ConfigParser()
config.read('config.ini')

s3_client = boto3.client(
    service_name='s3',
    endpoint_url='https://s3.{}.amazonaws.com/'.format(config.get('s3', 'region')),
    aws_access_key_id=os.environ['AWS_SECRET_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_KEY']
)

photo_metadata = {}


def main():
    image = capture_photo()
    if image:
        if not s3_bucket_exists():
            create_s3_bucket()
        upload_photo(image)


def save_photo_to_sd_card(photo_data):
    photo_data.save(photo_metadata['path'])


def capture_photo():
    output_stream = BytesIO()
    time = get_now_date()
    photo_metadata['filename'] = get_photo_filename(time)
    photo_metadata['path'] = '/home/pi/Pictures/{}'.format(photo_metadata['filename'])
    photo_metadata['readable_time'] = time.format(config.get('camera', 'watermark_format'))

    with PiCamera() as camera:
        try:
            # set camera
            camera.iso = int(config.get('camera', 'iso'))
            horizontal = int(config.get('camera', 'res_horizontal'))
            vertical = int(config.get('camera', 'res_vertical'))
            camera.resolution = (horizontal, vertical)
            camera.framerate = int(config.get('camera', 'framerate'))
            sleep(2)   # sleep because the camera needs to literally warm up. Give er' time!
            camera.shutter_speed = camera.exposure_speed
            camera.exposure_mode = config.get('camera', 'exposure_mode')
            g = camera.awb_gains
            camera.awb_mode = config.get('camera', 'awb_mode')
            camera.awb_gains = g
            camera.annotate_foreground = Color(config.get('camera', 'watermark_foreground'))
            camera.annotate_background = Color(config.get('camera', 'watermark_background'))
            camera.annotate_text = photo_metadata['readable_time']

            # capture the image
            camera.capture(output_stream, config.get('settings', 'file_format'))
            sleep(2)  # sleep because the camera needs to literally warm up. Give er' time!
            output_stream.seek(0)
            return output_stream.getvalue()

        except Exception as e:
            print("Capture Image Failure. Possibly intersection of two processes.")
            exit()

        finally:
            camera.close()


def get_photo_filename(time):
    return '{}.{}'.format(
        time.format(config.get('settings', 'picture_string_format')),
        config.get('settings', 'file_format')
    )


def upload_photo(image):
    try:
        bytes_stream = BytesIO(image)
        s3_client.upload_fileobj(
            bytes_stream,
            config.get('s3', 'main_bucket_name'),
            photo_metadata['filename']
        )
        return True
    except Exception as ex:
        return False


def create_s3_bucket():
    bucket_creation_response = s3_client.create_bucket(Bucket=config.get('s3', 'main_bucket_name'), CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    if bucket_creation_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def s3_bucket_exists():
    return config.get('s3', 'main_bucket_name') in [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]


def get_now_date():
    return arrow.utcnow().to(config.get('settings', 'timezone'))


if __name__ == '__main__':
    main()
