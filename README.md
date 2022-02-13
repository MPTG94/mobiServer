# MobiLapse Cloud Backend API repository

This repository is part of the [MobiLapse](https://github.com/MPTG94/Mobi-Lapse) project, specifically this repository
is dedicated to the Serverless backend REST API, including storage handling and image to video conversion functionality.

All exposed through a [flask](https://flask.palletsprojects.com/en/2.0.x/) python REST API

The Backend is run using Google Cloud Platform [Cloudrun](https://cloud.google.com/run)

## Requirements

* This project is built and deployed using [docker](https://www.docker.com/)
* Python version: Python 3.7+
* Additional needed libraries:
  * flask
  * gunicron
  * firebase_admin
  * opencv-python
  * marshmallow
  * google-cloud-storage
* The backend API also makes extensive use of Firebase services including Cloud Storage

  So in order to run the project properly you will need a `firebase.json` file 
  with information about your project (configurable in the `config.py` file)

## Running instructions

* In order to run the project, clone the repository using:

  ```git clone https://github.com/MPTG94/mobiServer.git mobiapi```

* After cloning, change the working directory to the project directory:

  ```cd mobiapi```

* Install the necessary pip packages listed above

* Run the REST API (which will invoke the rest of the functionality) using:

  ```python3 app.py```

**For instructions on deploying to the GCP Cloudrun platform please see below:**

(Note that the configured project name is `mobilapse` and you will need to change it to your GCP project)
## Building

`gcloud builds submit --tag gcr.io/mobilapse/mobiapi`

## Deploying

### Deploy cloud run instance

`gcloud run deploy --platform=managed --region=europe-west1 --image gcr.io/mobilapse/mobiapi mobiapicr`

## Combined

`gcloud builds submit --tag gcr.io/mobilapse/mobiapi && gcloud run deploy --platform=managed --region=europe-west1 --image gcr.io/mobilapse/mobiapi mobiapicr`