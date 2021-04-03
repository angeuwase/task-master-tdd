# Use official python docker base image
FROM python:3.8-slim

# Set the default working directory where the project will be installed on the container. HOME directory created when new user was created. Making the HOME directory the default directory
WORKDIR /app

# Copy the requirements.txt file over to the container. Source file location is relative to location of the Dockerfile. Destination can be absolute path or relative to WORKDIR
COPY requirements.txt requirements.txt

# Install installl dependencies. gunicorn (production WSGI server) has been added to requirements.txt file
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Install the project on the container.
COPY . .

# Configure the flask app for production
ENV FLASK_ENV = production

# Configure port 5000 to be the port that this container will be using for its server. This is necessary so that Docker can configure the network in the container appropriately.
EXPOSE 5000

# Run the server with gunicorn
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]

