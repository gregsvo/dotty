import arrow
import boto3
import csv
from picamera import PiCamera, Color
from time import sleep

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

photo = {}


def main():
    capture_photo()
    if not s3_bucket_exists():
        create_s3_bucket()
        upload_photo()
    save_photo_info()


def capture_photo():
    time = get_current_time()
    photo['filename'] = get_photo_filename(time)
    photo['path'] = '/home/pi/Pictures/{}'.format(photo['filename'])
    with PiCamera() as camera:
        camera.iso = 200
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
        camera.capture(photo['path'])
        sleep(2)
    photo['timestamp'] = time.timestamp


def get_photo_filename(time):
    return '{}.jpg'.format(time.timestamp)


def upload_photo():
    photo_data = open(photo['path'], 'rb')
    s3_resource.Bucket('dotty').put_object(Key=photo['filename'], Body=photo_data)
    # TODO: verify upload via boto3.exceptions.S3UploadFailedError
    photo['url'] = 'https://s3.{}.amazonaws.com/{}/{}'.format('us-east-2', 'dotty', photo['filename'])


def create_s3_bucket():
    bucket_creation_response = s3_client.create_bucket(Bucket='dotty', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    if bucket_creation_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True


def s3_bucket_exists():
    return 'dotty' in [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]


def save_photo_info():
    with open('photo_upload_list.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([photo['filename'], photo['url'], photo['timestamp']])


def get_current_time():
    return arrow.utcnow().to('US/Eastern')


if __name__ == '__main__':
    main()
