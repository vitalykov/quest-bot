BOT_IMAGE = quest-bot-image
BOT_CONTAINER = quest-bot-container

all: build run

build:
	docker build -t $(BOT_IMAGE) .

run:
	docker run -it -d --restart=unless-stopped --name $(BOT_CONTAINER) $(BOT_IMAGE)

start:
	docker container start $(BOT_CONTAINER)

stop:
	docker stop $(BOT_CONTAINER)

delete_container:
	docker rm $(BOT_CONTAINER)

delete_image:
	docker rmi $(BOT_IMAGE)
