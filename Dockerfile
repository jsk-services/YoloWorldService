FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

# Necessary for opencv-python to run in a docker container.
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Install dependency python pakcages.
RUN pip3 install grpcio grpcio-tools pymongo cachetools
RUN pip3 install opencv-python-headless openai-clip ultralytics

COPY yolo* .
COPY YoloWorldService* .

EXPOSE 9000

ENTRYPOINT ["python3", "yolo_world_server.py"]