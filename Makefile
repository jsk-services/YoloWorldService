IMAGE_NAME="jsk-services/yolo-world-service"
CONTAINER_NAME="yolo-world-service"
SERVICE_PORT=9000

build:
	docker build -t $(IMAGE_NAME) .

run: build
	docker run --gpus all --name $(CONTAINER_NAME) -p $(SERVICE_PORT):9000 -d $(IMAGE_NAME)

clean:
	docker stop $(CONTAINER_NAME) && docker remove $(CONTAINER_NAME) && docker rmi $(IMAGE_NAME)

rebuild: clean build