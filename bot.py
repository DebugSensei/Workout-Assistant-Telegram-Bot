from telegram.ext import Updater, CommandHandler
from telegram.ext import ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackContext, ConversationHandler,CallbackQueryHandler
import logging
import config
from handlers import start, status,workout_callback, done, help_command, workout, update_record,RECORD_TYPE,RECORD_VALUE,record_type,record_value,cancel,myrecords,send_music,friends
from telegram.ext import JobQueue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    updater = Updater(token=config.TOKEN, use_context=True)
    dp = updater.dispatcher
    job_queue = JobQueue()
    job_queue.set_dispatcher(dp)
    job_queue.start()
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("workout", workout))
    dp.add_handler(CommandHandler("myrecords", myrecords))
    dp.add_handler(CallbackQueryHandler(workout_callback, pattern='^(home|gym|workout)$'))
    dp.add_handler(CommandHandler("done", done))
    dp.add_handler(CommandHandler('phonk', send_music))
    dp.add_handler(CommandHandler("friends", friends))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('updaterecord', update_record)],
        states={
            RECORD_TYPE: [MessageHandler(Filters.text & ~Filters.command, record_type)],
            RECORD_VALUE: [MessageHandler(Filters.text & ~Filters.command, record_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(CommandHandler('cancel', cancel))
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
