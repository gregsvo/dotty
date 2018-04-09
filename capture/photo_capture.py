import arrow
import boto3
import csv
from picamera import PiCamera, Color
from time import sleep

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')


def main():
    time = get_current_time()
    filename_of_photo = capture_photo(time)
    if not s3_bucket_exists():
        create_s3_bucket()
    photo_url = upload_photo(filename_of_photo)
    save_photo_info(filename_of_photo, photo_url, time)


def capture_photo(time):
    save_location = '/home/pi/Pictures/'
    filename = '{}{}.jpg'.format(save_location, time.timestamp)
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
        camera.capture(filename)
        sleep(2)
        return filename


def upload_photo(filename_of_photo):
    photo_data = open(filename_of_photo, 'rb')
    s3_resource.Bucket('dotty').put_object(Key=filename_of_photo, Body=photo_data)
    # TODO: verify upload via boto3.exceptions.S3UploadFailedError
    photo_url = 'https://s3.{}.amazonaws.com/{}/{}'.format('us-east-2', 'dotty', filename_of_photo)
    return photo_url


def create_s3_bucket():
    bucket_creation_response = s3_client.create_bucket(Bucket='dotty', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    if bucket_creation_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True


def s3_bucket_exists():
    return 'dotty' in [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]


def save_photo_info(filename_of_photo, file_location_of_photo, time):
    filename = 'photo_upload_list.csv'
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow([filename_of_photo, file_location_of_photo, time.timestamp])


def get_current_time():
    return arrow.utcnow().to('US/Eastern')


if __name__ == '__main__':
    main()
