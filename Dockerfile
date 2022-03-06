FROM python:3.8-slim-buster

# Change working directory.
WORKDIR /app
# Update PIP.
RUN pip install --upgrade pip
# Install requirements from file.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Copy python scripts to container.
COPY *.py .
# Use entrypoint instead of CMD for being able to pass arguments to the container.
ENTRYPOINT ["python", "attack.py"]
