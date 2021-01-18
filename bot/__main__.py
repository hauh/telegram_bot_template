"""Template Bot."""

import logging

from telegram.constants import CHAT_PRIVATE
from telegram.error import NetworkError, TelegramError
from telegram.ext import (
	CommandHandler, DispatcherHandlerStop, Filters, Handler, MessageHandler
)

from bot import updater


class UpdateFilter(Handler):
	"""By default bot should be used only in private chats."""

	def __init__(self):
		super().__init__(callback=None)

	def check_update(self, update):
		if chat := update.effective_chat:
			if chat.type == CHAT_PRIVATE:
				return None
			logging.warning("Leaving %s '%s'.", chat.type, chat.title)
			chat.leave()
		raise DispatcherHandlerStop()


def start(update, _context):
	update.effective_chat.send_message("💜")


def clean(update, _context):
	update.effective_message.delete()


def error(update, context):
	error_info = f"{context.error.__class__.__name__}: {context.error}"
	if not update or not update.effective_user:
		logging.error("Bot %s", error_info)
	else:
		try:
			update.effective_message.delete()
		except (AttributeError, TelegramError):
			pass
		user = update.effective_user.username or update.effective_user.id
		logging.warning("User '%s' %s", user, error_info)
	start(update, context)


def main():
	dispatcher = updater.dispatcher
	dispatcher.add_handler(UpdateFilter())
	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(MessageHandler(Filters.all, clean))
	dispatcher.add_error_handler(error)

	try:
		updater.start_polling()
	except NetworkError:
		logging.critical("Connection failed.")
	else:
		logging.info("Bot started!")
		updater.idle()
		logging.info("Turned off.")


if __name__ == "__main__":
	main()
