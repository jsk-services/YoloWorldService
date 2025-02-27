# YoloWorldService
A microservice server for an open vocabulary object detection neural network, 
[YOLO-World](https://github.com/AILab-CVC/YOLO-World).

## Model

This server uses [Ultralytics](https://github.com/ultralytics/ultralytics) as inference engine,
model weights are downloaded from [Ultralytics YOLO-World](https://docs.ultralytics.com/models/yolo-world/),
no newer than July 3rd, 2024.

## Usage

### Detect

Use `Detect` method of `YoloWorldService` to get the positions of bounding boxes of specific classes of objects.

`ClientName` field of the `DetectionRequest` should be unique, as they are the identity to allocate and access model instance,
if two or more clients are using the same client name, then they will use the same model instance, 
and errors will occur if they are using different class names.

Image should be passed in the `JpegImage` field, in the form of bytes of JPEG format.

### Label

`Lable` method is basically same to `Detect` method, the only difference is this method is designed for quick test,
so it will return the result image where detected objects are labeled.

## Client

Package `yolo_world_client` provides a client class `YoloWorldClient`, 
which wraps the process of image encoding and decoding.

## Makefile

Use `make run` to build the Docker image and start a Docker container on your machine.

Use `make clean` to stop the container, and then delete the container and image from your machine.

You can customize the image and the container with following three variable of the Makefile:
- IMAGE_NAME: the tag of the image built by 'build' command.
- CONTAINER_NAME: the name of the container started by 'run' command.
- SERVICE_PORT: the port which the service will be listening on.
