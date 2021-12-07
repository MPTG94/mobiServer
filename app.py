import datetime
import logging
import sys
import traceback

import marshmallow.exceptions
from flask import Flask, request

from capture_handler import convert_downloaded_images_to_videos
from config import ENVIRONMENT, PORT, API_REQUEST_DATETIME_FORMAT, STORAGE_TARGET_DATETIME_FORMAT
from filesystem_handler import create_temp_dir
from request_validators import ConvertImagesToVideoSchema
from storage_handler import download_captured_images_to_temp_dir, upload_result_videos_to_bucket

logger = logging.getLogger('gcp_logger')

app = Flask(__name__)


@app.route('/')
def hello_world():
    response = {
        'message': 'API Alive',
        'Environment': ENVIRONMENT,
        'Port': PORT
    }
    return response, 200


@app.post('/convert')
def convert_images_to_video():
    try:
        data = ConvertImagesToVideoSchema().load(request.get_json())
        temp_dir = create_temp_dir()
        result_folder_list = download_captured_images_to_temp_dir(temp_dir, data['objects'], data['datetime'])
        timestamp_obj = datetime.datetime.strptime(data['datetime'], API_REQUEST_DATETIME_FORMAT)
        output_dir = convert_downloaded_images_to_videos(temp_dir, result_folder_list,
                                            timestamp_obj.strftime(STORAGE_TARGET_DATETIME_FORMAT))
        upload_result_videos_to_bucket(output_dir)
        return {'Status': 'Success',
                'Message': 'Finished converting images to video',
                'OutputFile': 'PLACEHOLDER'}, 200
    except marshmallow.exceptions.ValidationError as e:
        logger.warning('Validation error occurred')
        return {'Error': f'validation error occurred: {str(e)}'}
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        logger.warning(f'ERROR - {type(e)}: {e}')
        return {'Error': f'An error occurred: {e}'}, 500


if __name__ == '__main__':
    logger.warning("Running mobiAPI")
    if ENVIRONMENT.lower() == 'gcp':
        app.run(debug=True, host='0.0.0.0', port=PORT)
    else:
        print(f'running local, host: 127.0.0.1, port: {PORT}')
        app.run(debug=True, host='127.0.0.1', port=PORT)
