from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pytube
from io import BytesIO
import logging

updater = Updater(token='1072871384:AAFGbIjIt1OO4rnbMDqIIn1Sco3sZhjVW_8', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
	link = update.message.text
	yt = pytube.YouTube(link)
	stream = yt.streams.first()
	buf = stream.stream_to_buffer()
	print(buf)
	buf.seek(0)
	context.bot.send_video(chat_id=update.effective_chat.id, video = buf)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
