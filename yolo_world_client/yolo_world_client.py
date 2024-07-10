import cv2
import numpy as np
from typing import Iterable
from YoloWorldService_pb2 import *
from YoloWorldService_pb2_grpc import *

class YoloWorldClient:
    def __init__(self, client_name: str, service_address: str):
        self._name = client_name
        channel = grpc.insecure_channel(service_address)
        self._client = YoloWorldServiceStub(channel)

    @staticmethod
    def _encode_image(image: np.ndarray) -> bytes:
        success, data = cv2.imencode(".jpg", image)
        return data.tobytes()

    @staticmethod
    def _decode_image(data: bytes) -> np.ndarray:
        data = np.frombuffer(data, dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)

    def label(self, image: np.ndarray, class_names: Iterable[str]) -> np.ndarray:
        """
        Use YoloWorld to label objects with specific class names from an image with bounding boxes.
        :param image: Image to label objects from.
        :param class_names: Names of object classes.
        :return: Image with bounding boxes.
        """
        request = LabelRequest(
            ClientName=self._name,
            ClassNames=class_names,
            JpegImage=YoloWorldClient._encode_image(image),
        )
        response: LabelResponse = self._client.Label(request)
        return YoloWorldClient._decode_image(response.JpegImage)

    def detect(self, image: np.ndarray, class_names: Iterable[str]) -> Iterable[ObjectData]:
        """
        Detect objects with specific class names from an image.
        :param image: Image to detect objects from.
        :param class_names: Names of object classes to detect.
        :return: Information of detected objects, including class id, confidence, and bounding boxes.
        """
        request = DetectionRequest(
            ClientName=self._name,
            ClassNames=class_names,
            JpegImage=YoloWorldClient._encode_image(image),
        )
        response: DetectionResponse = self._client.Detect(request)
        return response.Objects
