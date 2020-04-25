from typing import Optional, List

from telegram import Update, Bot, Message, User, MessageEntity, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Handler, MessageHandler, Filters
from os import environ

# import logging

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.DEBUG)

challenge: Optional[List[str]] = None
challenge_from: Optional[int] = None
listen_to: Optional[int] = None

admins: [str] = []


def check_admin(user: User):
    return len(admins) == 0 or f"@{user.username}" in admins


def add_admin(username: str):
    if username is None or len(username) == 0:
        return
    if username not in admins:
        admins.append(username)


def del_admin(username: str):
    if username in admins:
        admins.remove(username)


def secure(method):
    def secured(update: Update, context: CallbackContext):
        msg: Message = update.message
        if not check_admin(msg.from_user):
            context.bot.send_message(msg.chat_id, f"You are not authorized for this command!")
            return
        method(update, context)

    return secured


def current_user(method):
    def secured(update: Update, context: CallbackContext):
        msg: Message = update.message
        if challenge_from is not None and challenge_from != msg.from_user.id:
            context.bot.send_message(msg.chat_id, f"You are not the current user!")
            return
        method(update, context)

    return secured


def private(method):
    def secured(update: Update, context: CallbackContext):
        msg: Message = update.message
        bot: Bot = context.bot

        msg_type: str = msg.chat.type  # 'private', 'group', 'supergroup' or 'channel'
        if msg_type != "private":
            bot.send_message(msg.chat_id, f"The command has to be executed in a private channel!")
            return

        method(update, context)

    return secured


def start(update: Update, context: CallbackContext):
    msg: Message = update.message
    bot: Bot = context.bot

    with open("README.md") as readme:
        bot.send_message(msg.chat_id, readme.read(), parse_mode=ParseMode.MARKDOWN)


@secure
def add_new_admin(update: Update, context: CallbackContext):
    msg: Message = update.message
    mentions = msg.parse_entities([MessageEntity.MENTION])
    if len(mentions) == 0:
        context.bot.send_message(msg.chat_id, "You haven't mentioned anyone!")
        return
    for m in mentions.values():
        add_admin(m)
        context.bot.send_message(msg.chat_id, f"Added {m}")


@secure
def remove_admin(update: Update, context: CallbackContext):
    msg: Message = update.message
    mentions = msg.parse_entities([MessageEntity.MENTION])
    if len(mentions) == 0:
        context.bot.send_message(msg.chat_id, "You haven't mentioned anyone!")
        return
    for m in mentions.values():
        del_admin(m)
        context.bot.send_message(msg.chat_id, f"Removed {m}")


@secure
def list_admins(update: Update, context: CallbackContext):
    msg: Message = update.message
    if len(admins) == 0:
        context.bot.send_message(msg.chat_id, "Everyone is admin")
    else:
        context.bot.send_message(msg.chat_id, f"Current admins: {', '.join(admins)}")


@secure
def state(update: Update, context: CallbackContext):
    msg: Message = update.message
    bot: Bot = context.bot

    msg_type: str = msg.chat.type  # 'private', 'group', 'supergroup' or 'channel'
    if msg_type != "private":
        bot.send_message(msg.chat_id, f"State command only allowed in private chat. This is a {msg_type} chat.")
        return

    bot.send_message(msg.chat_id, "I'm running ..")
    bot.send_message(msg.chat_id, f"Challenger: {challenge_from}, Challenge: {None if challenge is None else ', '.join(challenge)}")


@secure
def listen_here(update: Update, context: CallbackContext):
    global listen_to
    msg: Message = update.message
    bot: Bot = context.bot
    listen_to = msg.chat_id
    bot.send_message(msg.chat_id, f"Now I'm listening here ..")


@current_user
@private
def new_challenge(update: Update, context: CallbackContext):
    global challenge, challenge_from
    msg: Message = update.message
    bot: Bot = context.bot
    challenge_from = msg.from_user.id

    if listen_to is None:
        bot.send_message(msg.chat_id, "Please set listen_to first.")
        return

    if challenge is not None:
        bot.send_message(msg.chat_id, "Challenge already active ..")
        return

    txt: str = update.message.caption
    txt = txt[len('/new'):].strip()
    challenge = list(filter(lambda s: len(s) != 0, [x.lower().strip() for x in txt.split(",")]))
    bot.send_photo(listen_to, msg.photo[0].file_id, caption=f"Your next challenge from {msg.from_user.first_name} ... good luck :)")


def answer(update: Update, context: CallbackContext):
    global challenge, challenge_from
    msg: Message = update.message

    if msg is None or msg.chat_id != listen_to:
        return

    text: str = msg.text
    if text is None or challenge is None:
        return
    text = text.lower()

    for ch in challenge:
        if ch.lower() not in text:
            return

    context.bot.send_message(msg.chat_id, f"{str(msg.from_user.first_name)} got it: {', '.join(challenge)}")
    challenge = None
    challenge_from = msg.from_user.id


class NewHandler(Handler):
    def __init__(self, callback):
        super().__init__(callback)

    def check_update(self, update):
        msg: str = update.message.caption
        if msg is None or not msg.startswith("/new"):
            return False
        if update.message.photo is not None and len(update.message.photo) > 0:
            return True

        return False


@current_user
@private
def image_missing(update: Update, context: CallbackContext):
    msg: Message = update.message
    bot: Bot = context.bot
    bot.send_message(msg.chat_id, "The image is missing.")


def main():
    updater = Updater(environ["Token"], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), answer))

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('state', state))
    dp.add_handler(CommandHandler('add_admin', add_new_admin))
    dp.add_handler(CommandHandler('remove_admin', remove_admin))
    dp.add_handler(CommandHandler('admins', list_admins))

    dp.add_handler(CommandHandler('listen', listen_here))

    dp.add_handler(NewHandler(new_challenge))
    dp.add_handler(CommandHandler('new', image_missing))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
