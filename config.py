import os

PROJECT_ID = 'mobilapse'

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'GCP')
STORAGE_BUCKET = 'mobilapse.appspot.com'

API_REQUEST_DATETIME_FORMAT = '%d-%m-%YT%H-%M-%S'
STORAGE_TARGET_DATETIME_FORMAT = '%Y-%m-%dT%H-%M-%S'

PORT = 8080
if ENVIRONMENT.lower() == 'gcp':
    PORT = int(os.environ.get('PORT', 8080))
else:
    PORT = int(os.environ.get('PORT', 8080))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\1912m\\mobilapse-firebase-key.json'