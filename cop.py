from typing import Optional, List

from telegram import Update, Bot, Message, User, MessageEntity, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Handler, MessageHandler, Filters
from os import environ

# import logging

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.DEBUG)

from state import state
from helpers import current_user, private, admin


def start(update: Update, context: CallbackContext):
    msg: Message = update.message
    bot: Bot = context.bot

    with open("commands.md") as readme:
        bot.send_message(msg.chat_id, readme.read(), parse_mode=ParseMode.MARKDOWN)


@admin
def add_new_admin(update: Update, context: CallbackContext):
    msg: Message = update.message
    mentions = msg.parse_entities([MessageEntity.MENTION])
    if len(mentions) == 0:
        context.bot.send_message(msg.chat_id, "You haven't mentioned anyone!")
        return
    for m in mentions.values():
        state.add_admin(m)
        context.bot.send_message(msg.chat_id, f"Added {m}")


@admin
def remove_admin(update: Update, context: CallbackContext):
    msg: Message = update.message
    mentions = msg.parse_entities([MessageEntity.MENTION])
    if len(mentions) == 0:
        context.bot.send_message(msg.chat_id, "You haven't mentioned anyone!")
        return
    for m in mentions.values():
        state.del_admin(m)
        context.bot.send_message(msg.chat_id, f"Removed {m}")


@admin
def list_admins(update: Update, context: CallbackContext):
    msg: Message = update.message
    context.bot.send_message(msg.chat_id, state.get_admin_state())


@admin
def show_state(update: Update, context: CallbackContext):
    msg: Message = update.message
    bot: Bot = context.bot

    msg_type: str = msg.chat.type  # 'private', 'group', 'supergroup' or 'channel'
    if msg_type != "private":
        bot.send_message(msg.chat_id, f"State command only allowed in private chat. This is a {msg_type} chat.")
        return

    bot.send_message(msg.chat_id, state.__repr__())


@admin
def listen_here(update: Update, context: CallbackContext):
    msg: Message = update.message
    bot: Bot = context.bot
    contains = state.update_listen_to(msg.chat_id)
    bot.send_message(msg.chat_id, f"Now I'm listening here .." if contains else f"I'm not listening here anymore ..")


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
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), state.check_answer))

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('state', show_state))
    dp.add_handler(CommandHandler('add_admin', add_new_admin))
    dp.add_handler(CommandHandler('remove_admin', remove_admin))
    dp.add_handler(CommandHandler('admins', list_admins))

    dp.add_handler(CommandHandler('listen', listen_here))

    dp.add_handler(NewHandler(state.new_challenge))
    dp.add_handler(CommandHandler('new', image_missing))

    dp.add_handler(CommandHandler('skip', state.skip))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
