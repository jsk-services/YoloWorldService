import numpy

from YoloWorldService_pb2 import *
from YoloWorldService_pb2_grpc import *
import cv2

if __name__ == '__main__':

    SERVICE_ADDRESS = ''

    channel = grpc.insecure_channel(SERVICE_ADDRESS)
    client = YoloWorldServiceStub(channel)

    camera = cv2.VideoCapture(0)
    while cv2.waitKey(1) != 27:
        success, frame = camera.read()
        if not success:
            continue
        success, data = cv2.imencode(".jpg", frame)
        request = LabelRequest(
            ClientName="test",
            ClassNames=["person", "watch"],
            JpegImage=data.tobytes()
        )
        response: LabelResponse = client.Label(request)
        data = numpy.frombuffer(response.JpegImage, dtype=numpy.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("test", image)