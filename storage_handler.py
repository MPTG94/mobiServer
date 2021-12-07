import logging
import os

import firebase_admin
from firebase_admin import storage
from google.cloud.storage import Blob

from config import STORAGE_BUCKET
from filesystem_handler import create_sub_folders_in_path

CAPTURED_IMAGES_ROOT_PATH = 'robotImages/'
# VIDEO_CONTENT_TYPE = 'video/webm'
VIDEO_CONTENT_TYPE = 'video/mp4'

logger = logging.getLogger('gcp_logger')

default_app = firebase_admin.initialize_app(credential=None, options={'storageBucket': STORAGE_BUCKET})

bucket = storage.bucket()


def download_captured_images_to_temp_dir(dir_path, num_objects, timestamp):
    folder_list = build_source_folder_list(num_objects, timestamp)
    blob: Blob
    for blob in bucket.list_blobs(prefix='robotImages/'):
        if blob.name.endswith('/'):
            # Skipping dirs
            continue
        if not blob.name.rsplit('/', 1)[0] in folder_list:
            # Skipping folders we don't want
            continue
        target_file_path = os.path.join(dir_path, blob.name)
        create_sub_folders_in_path(os.path.dirname(target_file_path))
        logger.warning(f'Downloading {blob.name} to {target_file_path}')
        blob.download_to_filename(target_file_path)
    return folder_list


def build_source_folder_list(num_objects, timestamp):
    folder_list = []
    for i in range(1, num_objects + 1):
        folder_list.append(f'{CAPTURED_IMAGES_ROOT_PATH}object{i}CaptureSession-{timestamp}')
    return folder_list


def upload_result_videos_to_bucket(output_path):
    print(output_path)
    for dirpath, _, videos in os.walk(output_path):
        for video in videos:
            upload_video(video, os.path.join(dirpath, video))


def upload_video(video_name, video_path):
    blob = bucket.blob(f'captures/{video_name}')
    logger.warning(f'Uploading {video_name} to captures/{video_name} from {video_path}')
    blob.upload_from_filename(video_path, content_type=VIDEO_CONTENT_TYPE)
