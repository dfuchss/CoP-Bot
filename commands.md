Challenge of Pic (Telegram Bot)

A simple "challenge of pictures bot". Your task is to guess the terms of a picture.

For admins:
```
/state: Get the current state of the bot
/add_admin [UserMentions]: promote users
/remove_admin [UserMentions]: demote users 
/admins: show all admins
/listen: select the group channel for listening or not listening
/skip: allows the current user to skip the challenge
```

For all players:
```
/help: This message here <----
/skip: allows the current user to skip the challenge
/highscore: get the current high scores
/new Word1,Word2;Alternative;Alternative2 ... as caption of an image sent via a private channel: Create a new challenge you have to find all the words separated by ','. Different alternatives can indicated via ';' (similar to Prolog)
/refine Word1,Word2;Alternative;Alternative2 ... sent via a private channel: Update challenge. Same format as /new.
```
