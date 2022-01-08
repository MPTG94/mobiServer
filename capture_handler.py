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
        # source_images_filter = f'{os.path.join(dir_path, folder)}{os.path.sep}*.jpg'
        # The robot captures png images
        source_images_filter = f'{os.path.join(dir_path, folder)}{os.path.sep}*_crop.png'
        target_size = None
        filter_list = glob.glob(source_images_filter)
        # ################## TODO
        print(filter_list)
        sorted(filter_list, key=lambda x: int(x[:-4]))
        print(filter_list)
        # ################## TODO
        for filename in filter_list:
            print(filename)
            img = cv2.imread(filename)
            height, width, layers = img.shape
            target_size = (width, height)
            img_list.append(img)
        # For webm files (can be played by browser and android)
        output_video_name = f'capture_{curr_capture}_{datetime}.webm'
        out = cv2.VideoWriter(os.path.join(target_directory, output_video_name),
                              cv2.VideoWriter_fourcc(*'vp80'), 1, target_size)
        # For mp4 files (can be played by android)
        # output_video_name = f'capture_{curr_capture}_{datetime}.mp4'
        # out = cv2.VideoWriter(os.path.join(target_directory, output_video_name),
        #                       cv2.VideoWriter_fourcc(*'MP4V'), 1, target_size)
        # For avi files (can be played by android)
        # output_video_name = f'capture_{curr_capture}_{datetime}.avi'
        # out = cv2.VideoWriter(os.path.join(target_directory, output_video_name),
        #                       cv2.VideoWriter_fourcc(*'MJPG'), 1, target_size)
        for i in range(len(img_list)):
            img = cv2.resize(img_list[i], target_size)
            out.write(img)
        out.release()
        logger.warning(
            f'Created video: {output_video_name} at path: {target_directory}')
        curr_capture += 1
        img_list = []
    return target_directory


def crop_and_adjust_img_to_img(prev_img_path, target_img_path) -> str:
    margin = 71
    if prev_img_path is None or prev_img_path == '':
        # first img just crop into its center
        ref_img = cv2.imread(target_img_path, cv2.IMREAD_COLOR)
        img_final_color = ref_img[margin: -margin,  margin:-margin]
        tmp_index = target_img_path.index('.png')
        crop_img_name = target_img_path[:tmp_index] + '_crop.png'
        cv2.imwrite(crop_img_name, img_final_color)
        return crop_img_name

    # loading the imgs in gray for the coming matching method
    img_to_crop = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
    ref_img = cv2.imread(prev_img_path, cv2.IMREAD_GRAYSCALE)

    height, weight = ref_img.shape
    # finding the best location which the imgs are corresponding together
    res_locs = cv2.matchTemplate(img_to_crop, ref_img, cv2.TM_CCOEFF)
    # min_val, max_val, min_loc, top_left = cv2.minMaxLoc(res_locs)
    top_left = cv2.minMaxLoc(res_locs)[-1]

    # save a copy of the img (with color) with crop according to the location we found
    tmp_index = target_img_path.index('.png')
    img_to_crop_color = cv2.imread(target_img_path, cv2.IMREAD_COLOR)
    img_final_color = img_to_crop_color[top_left[1]
        :top_left[1]+height, top_left[0]: top_left[0]+weight]
    crop_img_name = target_img_path[:tmp_index] + '_crop.png'
    cv2.imwrite(crop_img_name, img_final_color)
    return crop_img_name


def crop_and_adjust(dir_path, result_folder_list):
    target_directory = os.path.join(dir_path, 'output')
    create_sub_folders_in_path(target_directory)
    for folder in result_folder_list:
        # source_images_filter = f'{os.path.join(dir_path, folder)}{os.path.sep}*.jpg'
        # The robot captures png images
        source_images_filter = f'{os.path.join(dir_path, folder)}{os.path.sep}*.png'
        prev_filename = None
        filter_list = glob.glob(source_images_filter)
        # ################## TODO
        print(filter_list)
        sorted(filter_list, key=lambda x: int(x[:-4]))
        print(filter_list)
        # ################## TODO

        for filename in filter_list:
            if 'crop' in filename:
                continue
            prev_filename = crop_and_adjust_img_to_img(
                prev_img_path=prev_filename, target_img_path=filename)
