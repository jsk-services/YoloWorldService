build:
	docker build -t jsk-services/yolo-world-service .

run: build
	docker run --gpus all --name yolo-world-service -p 9000:9000 -d jsk-services/yolo-world-service

clean:
	docker stop yolo-world-service && docker remove yolo-world-service && docker rmi jsk-services/yolo-world-service

rebuild: clean build