# MobiAPI
REST api and advanced backend services for MobiLapse project

## Building

`gcloud builds submit --tag gcr.io/mobilapse/mobiapi`

## Deploying

### Deploy cloud run instnce

`gcloud run deploy --platform=managed --region=europe-west1 --image gcr.io/mobilapse/mobiapi mobiapicr`