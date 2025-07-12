# Quest Bot
Telegram bot for quests

## Build and run
Maybe you will need to add `sudo` to the commands above 

To build docker image and container and instantly run the bot:
```commandline
make
```

To build docker image with bot:
```commandline
make build
```

To make container and run bot:
```commandline
make run
```

To stop the bot:
```commandline
make stop
```

To start the already built container with bot
```commandline
make start
```

To delete existing container with bot
```commandline
make delete_container
```

To delete existing image
```commandline
make delete_image
```