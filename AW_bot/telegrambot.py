import logging
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.ext import CommandHandler
import re


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="hey i am a bot for AW context \n please send me your download box")


async def echo(update: Update, context: ContextTypes):

    text = update.message.text_html_urled
    listofquality = []
    for i in range(5):
        listofquality.append([])
    print(text)
    quality = re.findall(
        r'<a href=(.*?)>(.{4})', text)
    print(quality)

    menu = []
    list2 = []
    dictqu = {0: '480', 1: '720', 2: '1080', 3: '2160'}
    for w in quality:
        w = list(w)
        w[1] = re.split('<', w[1])[0]
        if w[1] == '480' or w[1] == '480p':
            listofquality[0].append(w[0])
        if w[1] == '720' or w[1] == '720p':
            listofquality[1].append(w[0])
        if w[1] == '1080' or w[1] == '1080p':
            listofquality[2].append(w[0])
        if w[1] == '2160' or w[1] == '2160p':
            listofquality[3].append(w[0])

    for w in listofquality:
        print(w, len(w))

    for i in range(4):
        if len(listofquality[i]) > 0:
            list2.append(dictqu[i])
    list2 = set(list2)
    for i in list2:
        but = [telegram.InlineKeyboardButton(i, callback_data=i)]
        menu.append(but)

    markup = telegram.InlineKeyboardMarkup(menu)

    await context.bot.send_message(chat_id=update.effective_chat.id, text='please send me what quality you want', reply_markup=markup)

    # await context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id='', message_id=)


async def forwardanime(update: Update, context: ContextTypes):
    ans = update.callback_query.data

    dcitqu = {'480': 0, '720': 1, '1080': 2, '2160': 3}

    quality = dcitqu[ans]

    print(quality)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=(ans, quality))

if __name__ == '__main__':
    application = ApplicationBuilder().token(
        'bot_token').build()
    
    
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    fanimehandler = CallbackQueryHandler(forwardanime)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(fanimehandler)
    application.run_polling()

