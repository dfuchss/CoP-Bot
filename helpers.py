from telegram import Update, Message, Bot
from telegram.ext import CallbackContext

from state import state


def admin(method):
    def secured(update: Update, context: CallbackContext):
        msg: Message = update.message
        if not state.check_admin(msg.from_user):
            context.bot.send_message(msg.chat_id, f"You are not authorized for this command!")
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


def current_user(method):
    def secured(update: Update, context: CallbackContext):
        msg: Message = update.message
        if not state.challenge_from(msg.from_user):
            context.bot.send_message(msg.chat_id, f"You are not the current user!")
            return
        method(update, context)

    return secured
