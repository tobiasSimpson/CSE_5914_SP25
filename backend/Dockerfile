# Dockerfile for flask react app
FROM python:3.12-slim

# Set the working directory
WORKDIR /backend
COPY pip-requirements.txt /backend
RUN pip3 install -r pip-requirements.txt

COPY . .
EXPOSE 5000
CMD [ "python3", "rest_api.py" ]