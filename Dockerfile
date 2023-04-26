# Use the official Python image as the base image
FROM python:3.8

RUN pip install --root-user-action=ignore requests

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

EXPOSE 8000/tcp
# Define the entry point for the container
CMD ["python", "py.py", "runserver", "0.0.0.0:8000"]
