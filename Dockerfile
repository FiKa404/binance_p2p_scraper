# Use the official Python image as the base image
FROM python:3.8

RUN pip install --upgrade pip

RUN adduser -D myuser
USER myuser
WORKDIR /home/myuser

COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/myuser/.local/bin:${PATH}"

COPY --chown=myuser:myuser . .

# Define the entry point for the container
CMD ["python", "py.py", "runserver", "0.0.0.0:8000"]
