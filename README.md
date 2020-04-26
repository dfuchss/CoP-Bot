# Challenge of Pic (Telegram Bot)
A simple "challenge of pictures bot". Your task is to guess the terms of a picture.

## Commands (see [commands.md](commands.md))
## Requirements (Development):
- python3 with pip
- `pip install -r requirements.txt`

## Run the Bot (via Docker)

You'll need the following two things:
* The possibility to run a docker container
* A Telegram Bot Account (set privacy mode to 'false' @ BotFather)

Then simply run ``docker build -t cop-bot .`` to build a docker image of the bot.
 
To start the bot simply run:
```
docker run -d \
    --env Token="Your Token" \
cop-bot
 ```

Optionally you can map the config for persistence:
```
docker run -d \
    --env Token="Your Token" \
    --mount type=bind,source=/path_to_existing/cop-state.json,target=/usr/src/app/state.json \
cop-bot
 ```

