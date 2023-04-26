# Use the official Python image as the base image
FROM python:3.8

RUN pip install --upgrade pip

RUN pip install --root-user-action=ignore requests

# Copy everything...
COPY . ./
# See everything (in a linux container)...
RUN dir -s    

EXPOSE 8000/tcp
# Define the entry point for the container
CMD ["python", "py.py", "0.0.0.0:8000"]
