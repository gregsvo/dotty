import arrow
import boto3
import csv
from picamera import PiCamera, Color
from time import sleep
from io import BytesIO
from PIL import Image


s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

photo_metadata = {}


def main():
    in_mem_photo = capture_photo()
    if in_mem_photo:
        if not s3_bucket_exists():
            create_s3_bucket()
        upload_photo(in_mem_photo)
        save_photo_info()


def capture_photo():
    print('capturing photo')
    photo_stream = BytesIO()
    in_mem_photo = BytesIO()
    time = get_current_time()
    photo_metadata['filename'] = get_photo_filename(time)
    photo_metadata['path'] = '/home/pi/Pictures/{}'.format(photo_metadata['filename'])
    photo_metadata['timestamp'] = time.timestamp
    photo_metadata['readable_time'] = time.format('MM/DD/YYYY : hh:mm a')

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
        camera.annotate_text = photo_metadata['readable_time']
        camera.capture(photo_stream, format='jpeg')
        sleep(2)
        photo_stream.seek(0)
        photo_data = Image.open(photo_stream)
        photo_data.save(in_mem_photo, format='jpeg')
        in_mem_photo.seek(0)
    return in_mem_photo


def get_photo_filename(time):
    print('creating filename')
    return '{}.jpg'.format(time.timestamp)


def upload_photo(in_mem_photo):
    print('uploading photo')
    s3_resource.Bucket('dotty').put_object(Key=photo_metadata['filename'], Body=in_mem_photo)
    # TODO: verify upload via boto3.exceptions.S3UploadFailedError
    photo_metadata['url'] = 'https://s3.{}.amazonaws.com/{}/{}'.format('us-east-2', 'dotty', photo_metadata['filename'])
    print("UPLOAD SUCCESSFUL: {}".format(photo_metadata['url']))


def create_s3_bucket():
    print('creating S3 bucket')
    bucket_creation_response = s3_client.create_bucket(Bucket='dotty', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    if bucket_creation_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def s3_bucket_exists():
    print('confirming bucket exists')
    return 'dotty' in [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]


def save_photo_info():
    with open('photo_upload_list.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([photo_metadata['readable_time'], photo_metadata['filename'], photo_metadata['url']])


def get_current_time():
    return arrow.utcnow().to('US/Eastern')


if __name__ == '__main__':
    main()
