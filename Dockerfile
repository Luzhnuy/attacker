FROM python:3.8-slim-buster
RUN apt-get update
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "attack_docker.py", "-t http://nlmk.com"]

# If you need add target
#ENTRYPOINT [ "python", "attack_docker.py", "-t http://nlmk.com"]
