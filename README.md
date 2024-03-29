# Challenge of Pic (Telegram Bot)
The bot helps with playing a simple picture challenge with your friends over telegram.
Someone starts by sending a picture and the word or phrase to guess. The other players
have to guess the phrase and the first to do so will have the right to post a new challenge.

## Features
- only the winning player can pose a new image challenge
- the active player can /skip their turn or stop the current challenge
- a high score is tracked

## Commands (see [commands.md](commands.md))
## Requirements (Development):
- python3 with pip
- `pip install -r requirements.txt`

## Run the Bot (via Docker)

You'll need the following two things:
* The possibility to run a docker container
* A Telegram Bot Account (set privacy mode to 'false' @ BotFather)

<!-- Then simply run ``docker build -t cop-bot .`` to build a docker image of the bot. -->
 
To start the bot simply run:
```
docker run -d \
    --env Token="Your Token" \
ghcr.io/dfuchss/copbot
 ```

Optionally you can map the config for persistence:
```
docker run -d \
    --env Token="Your Token" \
    --mount type=bind,source=/path_to_existing/cop-state.json,target=/usr/src/app/state.json \
ghcr.io/dfuchss/copbot
 ```

