import os
from concurrent import futures
from datetime import datetime
import cv2
import grpc
import numpy
import pymongo
from cachetools import cached, LRUCache
from ultralytics import YOLO

import YoloWorldService_pb2_grpc
from YoloWorldService_pb2 import *

SETTINGS_MODEL_NAME = os.environ.get('SETTINGS_MODEL_NAME', 'yolov8x-worldv2.pt')
SETTINGS_MAX_THREADS = os.environ.get('SETTINGS_MAX_THREADS', 10)
SETTINGS_MODEL_COUNT = os.environ.get('SETTINGS_MODEL_COUNT', 10)
SETTINGS_LOG_DATABASE = os.environ.get('SETTINGS_LOG_DATABASE', None)


class YoloWorldServer(YoloWorldService_pb2_grpc.YoloWorldServiceServicer):
    @cached(LRUCache(maxsize=SETTINGS_MODEL_COUNT))
    def get_model(self, client_name: str):
        self.log(f"Creating model for {client_name}")
        model = YOLO(SETTINGS_MODEL_NAME)
        self.log(f"Model {SETTINGS_MODEL_NAME} for {client_name} has been created.")
        return model

    def __init__(self):
        self._logger = None
        if SETTINGS_LOG_DATABASE != "" and SETTINGS_LOG_DATABASE is not None:
            self._logger = pymongo.MongoClient(SETTINGS_LOG_DATABASE)["logs"]["yolo_world"]

        self.log("Server instance instantiated.")

    def log(self, message: str, **kwargs):
        if self._logger is None:
            print(message)
            print(kwargs)
            return
        self._logger.insert_one({
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "message": message,
            "data": kwargs})

    def Detect(self, request: DetectionRequest, context) -> DetectionResponse:
        self.log("Detection request received.",
                 bytes_size=len(request.JpegImage),
                 client=request.ClientName)
        image = cv2.imdecode(numpy.frombuffer(request.JpegImage, dtype=numpy.uint8), cv2.IMREAD_COLOR)
        self.log("Original image decoded.", shape=image.shape)
        model = self.get_model(request.ClientName)
        model.set_classes(request.ClassNames)
        results = model.predict(image)[0]
        count = len(results.boxes)
        response = DetectionResponse()
        response.Objects.extend([
                ObjectData(
                    ClassId=int(results.boxes.cls[index]),
                    Confidence=float(results.boxes.conf[index]),
                    CenterX=float(results.boxes.xywh[index, 0]),
                    CenterY=float(results.boxes.xywh[index, 1]),
                    BoundingWidth=float(results.boxes.xywh[index, 2]),
                    BoundingHeight=float(results.boxes.xywh[index, 3])
                ) for index in range(count)
            ])
        self.log("Detection finished.")
        return response

    def Label(self, request: LabelRequest, context) -> LabelResponse:
        self.log("Label request received.",
                 bytes_size=len(request.JpegImage),
                 client=request.ClientName)
        image = cv2.imdecode(numpy.frombuffer(request.JpegImage, dtype=numpy.uint8), cv2.IMREAD_COLOR)
        self.log("Original image decoded.", shape=image.shape)
        model = self.get_model(request.ClientName)
        model.set_classes(request.ClassNames)
        results = model.predict(image)[0]
        image = results.plot()
        response = LabelResponse()
        response.JpegImage = cv2.imencode(".jpg", image)[1].tobytes()
        self.log("Label finished.")
        return response


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=SETTINGS_MAX_THREADS))
    YoloWorldService_pb2_grpc.add_YoloWorldServiceServicer_to_server(YoloWorldServer(), server)
    server.add_insecure_port(f'[::]:9000')
    server.start()

    print(f"Server started on port 9000.")

    server.wait_for_termination()

    print(f"Server terminated.")
