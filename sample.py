from yolo_world_client import YoloWorldClient
import cv2


if __name__ == '__main__':
    client = YoloWorldClient("test", "YOUR_SERVICE_ADDRESS")

    camera = cv2.VideoCapture(0)
    while cv2.waitKey(1) != 27:
        succeeded, image = camera.read()
        if not succeeded:
            continue
        result = client.label(image, ["person"])
        cv2.imshow("result", result)