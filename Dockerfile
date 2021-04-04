# Dockerfile for production application


# Use official python docker base image
FROM python:3.8-slim

# Set the default working directory of the project on the container
WORKDIR /app

# Copy the requirements.txt file over to the container. 
COPY requirements.txt requirements.txt

# Install dependencies and gunicorn (production WSGI server) 
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Install the project on the container.
COPY . .

# Configure the flask app for production
ENV FLASK_ENV = production
ENV CONFIG_TYPE = config.ProductionConfig

# Run database migration
RUN flask db init
RUN flask db migrate -m 'final migration'
RUN flask db upgrade

# Configure the container to listen to requests on port 5000. This is necessary so that Docker can configure the network in the container appropriately.
EXPOSE 5000

# Run the server with gunicorn
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]

