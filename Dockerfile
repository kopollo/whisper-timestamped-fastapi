FROM python:3.9

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg

RUN python3 -m pip install --upgrade pip

# Python installation
WORKDIR /usr/src/app

# Note: First installing the python requirements permits to save time when re-building after a source change.
COPY requirements.txt /usr/src/app/requirements.txt
RUN cd /usr/src/app/ && pip3 install -r requirements.txt

# Copy source
COPY . /usr/src/app/

ENTRYPOINT ["python", "client.py"]
