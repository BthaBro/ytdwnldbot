from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Chat, ChatAction
import pytube
from io import BytesIO
import logging

# Eanble logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

SETTINGS, VIDEO  = range(2)

def start(update, context): # start command
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello {}✌️. I can download videos and audios from youtube😎.".format
        (update.message.from_user.first_name))


def video(update, context): # video
    reply_keyboard = [['720p','360p']] # reply keyboard for quality

    update.message.reply_text('Please choose the quality of video\nOr send /cancel to cancel', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SETTINGS

itg = 0
def video_set(update, context): # video settings
    user = update.message.from_user
    quality = update.message.text
    global itg
    if quality == '720p':
        itg = '22'
    elif quality == '360p':
        itg = '18'
    logger.info("User  %s chose %s", user.first_name, update.message.text)
    update.message.reply_text('Now send me the link please', reply_markup = ReplyKeyboardRemove())

    return VIDEO


def video_send(update, context): # sending video
    link = update.message.text
    user = update.message.from_user
    logger.info("User %s sent %s", user.first_name, update.message.text)
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Accessing youtube link...")
    try:
        video = pytube.YouTube(link).streams.get_by_itag(itg)
    except:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Oops, something went wrong.\nMaybe there's no available with that quality.")
        return ConversationHandler.END
    else:
        title = video.title
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Fetching: {}...".format(title))
        buf = video.stream_to_buffer()
        print(buf)
        buf.seek(0)
        context.bot.send_chat_action(chat_id = update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)
        context.bot.send_video(chat_id = update.effective_chat.id, video = buf)
        context.bot.send_message(chat_id = update.effective_chat.id, text = "If bot has not sent you a video, file size of video might be more than 50 MB")
    return ConversationHandler.END


def cancel(update, context): # cancel command for video command
    user = update.message.from_user
    logger.info("User %s used /cancel", user.first_name)
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

AUDIO = range(1)

def audio(update, context):
    user = update.message.from_user
    logger.info("User %s called /audio comand", user.first_name)
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Send me a link for audio track")

    return AUDIO


def audio_send(update, context):
    user = update.message.from_user
    link = update.message.text
    logger.info("User %s sent %s", user.first_name, link)
    if 'youtu' not in link:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "It's not a valid link.")
    else:
        try:
            yt = pytube.YouTube(link)
            stream = yt.streams.filter(only_audio=True).first()
        except:
            context.bot.send_message(chat_id = update.effective_chat.id, text = "Oops, seems like there was an error")
        else:
            buf = stream.stream_to_buffer()
            print(buf)
            buf.seek(0)
            context.bot.send_audio(chat_id = update.effective_chat.id, audio = buf)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def main(): # main fuction
    updater = Updater(token='983360652:AAHBOs8EyivOVeOYgt7nM7LSxzY-x7J5nKM', use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
    dp = updater.dispatcher
    # start command
    dp.add_handler(CommandHandler('start', start))
    conv_handler_video = ConversationHandler(
        entry_points=[CommandHandler('video', video)],

        states = {
            SETTINGS : [MessageHandler(Filters.regex('^(720p|360p)$'), video_set)],
            VIDEO : [MessageHandler(Filters.text, video_send)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    conv_handler_audio = ConversationHandler(
    entry_points=[CommandHandler('audio', audio)],

    states = {
        AUDIO : [MessageHandler(Filters.text, audio_send)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler_audio)
    dp.add_handler(conv_handler_video)
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('help', help))

    # start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
