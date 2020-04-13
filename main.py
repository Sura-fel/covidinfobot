import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from covid import Covid

covid = Covid()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


start_var = """
This is a specfic purpose bot to help people get the real information regarding covid.
"""

help_var = """
Command : use
/start  : starts or update the bot.
/help   : shows this menu.
/ethio  : shows Ethiopia's status
/covid  : shows general data
/about  : who is the author
"""

about_var = """
Programmer : @met_asploit
Graphics : @met_asploit
manager : @met_asploit
"""


def start(update, context):
    update.message.reply_text(start_var)


def helps(update, context):
    update.message.reply_text(help_var)


def about(update, context):
    update.message.reply_text(about_var)


def ethio(update, context):
    update.message.reply_text(get_info('Ethiopia'))

def get_info(name):
    cov_info = covid.get_status_by_country_name(name)
    cou = 'COUNTRY -> ' + cov_info['country'] + '\n'
    ido = 'ID -> ' + str(cov_info['id']) + '\n'
    co = 'CONFRIMED CASES -> ' + str(cov_info['confirmed']) + '\n'
    ac = 'ACTIVE CASES -> ' + str(cov_info['active']) + '\n'
    he = 'HEALED (RECOVERED) -> ' + str(cov_info['recovered']) + '\n'
    de = 'DEATHS -> ' + str(cov_info['deaths'])
    
    return (cou + ido + co + ac + he + de)


def covi(update, context):
    update.message.reply_text('on development')

def list_cou(update, context):
    covid = Covid()
    countries = covid.list_countries()
    cou_var= [country['name'] for country in countries]
    cou_var.sort()
    le = len(cou_var)//2
    to_half = '\n'.join(cou_var[:le])
    to_end = '\n'.join(cou_var[le:])
    
    update.message.reply_text(to_half)
    update.message.reply_text(to_end)


def othr(update, context):
    countr = update.message.text
    covid = Covid()
    b = covid.list_countries()
    a = [co['name'] for co in b]
    if countr in a:
        update.message.reply_text(get_info(countr))
    else:
        update.message.reply_text('Country not found, use /list to list all country names')
        
def error(update, context):
    logger.warning('Update "%s" cad error "%s"', update, context.error)

def main():
    updater = Updater("1155995106:AAGjHQuvE8jQeeAGVYlrQTSN-KNZydVpkyU", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helps))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("ethio", ethio))
    dp.add_handler(CommandHandler("covid", covi))
    dp.add_handler(CommandHandler("list", list_cou))
    dp.add_handler(MessageHandler(Filters.text, othr))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
