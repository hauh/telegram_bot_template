"""Template Bot."""

import logging

from telegram.error import NetworkError, TelegramError
from telegram.ext import Filters, MessageHandler

from bot import updater


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


def echo(update, _context):
	update.effective_chat.send_message(update.effective_message.text)


def main():
	dispatcher = updater.dispatcher
	dispatcher.add_handler(MessageHandler(Filters.text, echo))
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
