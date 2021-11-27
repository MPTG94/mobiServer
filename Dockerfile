# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Copy local code to the container image.
ENV ENVIRONMENT 'GCP'
ENV DEPLOYMENT 'Production'
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip3 install Flask gunicorn
RUN pip3 install opencv-python
RUN pip3 install marshmallow
RUN pip3 install --upgrade google-cloud-storage
RUN pip3 install firebase-admin

# Run the web service on container startup. Here we use the gunicorn
# webserver, with 4 worker process and 4 threads.
CMD exec gunicorn --bind :$PORT --workers 4 --threads 4 app:app