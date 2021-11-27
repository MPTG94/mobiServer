import glob
import logging
import os

import cv2

from filesystem_handler import create_sub_folders_in_path

logger = logging.getLogger('gcp_logger')


def convert_downloaded_images_to_videos(dir_path, result_folder_list, datetime: str):
    img_list = []
    target_directory = os.path.join(dir_path, 'output')
    create_sub_folders_in_path(target_directory)
    curr_capture = 1
    for folder in result_folder_list:
        source_images_filter = f'{os.path.join(dir_path, folder)}{os.path.sep}*.jpg'
        target_size = (1280, 720)
        for filename in glob.glob(source_images_filter):
            print(filename)
            img = cv2.imread(filename)
            height, width, layers = img.shape
            img_list.append(img)
        output_video_name = f'capture_{curr_capture}_{datetime}.avi'
        out = cv2.VideoWriter(os.path.join(target_directory, output_video_name),
                              cv2.VideoWriter_fourcc(*'MJPG'), 1, target_size)
        for i in range(len(img_list)):
            img = cv2.resize(img_list[i], target_size)
            out.write(img)
        out.release()
        logger.warning(f'Created video: {output_video_name} at path: {target_directory}')
        curr_capture += 1
        img_list = []
    return target_directory