# -*- coding: utf-8 -*-
"""
@author: shuhratjon.khalilbekov@ru.ey.com
"""

"""
    0. Configuration
"""
config_path = 'C:/Users/Shuhratjon.Khalilbek/Downloads/gobot_w_slotfiller_v4/gobot_w_slots_and_db.json'

# set token from bot father
token = '1303155506:AAERVKH5kcRbZ3YFLxSJbMQFLjnATeKrMo8'

"""
    1. Modules and functions
"""
import json
from deeppavlov import build_model
from deeppavlov.dataset_readers.dstc2_reader import SimpleDSTC2DatasetReader
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class AssistantDatasetReader(SimpleDSTC2DatasetReader):
    
    # set path
    data_path = r'C:\Users\Shuhratjon.Khalilbek\Downloads\gobot_w_slotfiller_v3\/' 
   
    @staticmethod
    def _data_fname(datatype):
        assert datatype in ('val', 'trn', 'tst'), "wrong datatype name"
        return f"adhoc-dstc2-{datatype}.json"

def start(update, context):
    """
    function to return message for comman /start in telegram
    """
    update.message.reply_text(
        "По все вопросам пишите: @kshurik \n\n "
        "Добро пожаловать в бета версию интеллектуального помощника EY!")

def help_command(update, context):
    """
    function to return some text if /help command is sent by user in telegram    
    """
    update.message.reply_text('На данном этапе я могу помочь Вам узнать количество дней и забронированные дни отпуска, найти контакты и помочь с запросами в EY Help')

def load_model():
    """
    function to load model for usage
    """
    global gobot
    gobot = build_model(gobot_config, download=False)
    print('Model is built')

def custom_gobot(update, context):
    """
    function to get response from bot for a given text    
    """
    
    # get input text from user
    input_text = update.message.text.encode('utf-8').decode()

    # make it list if str
    input_text = [input_text] if isinstance(input_text, str) else input_text

    # get response from pretrained Go-Bot
    response = gobot(input_text)

    # modify response to appropiate type
    if len(response[0]) >= 2:
        response = response[0][1]
    else:
        response = response[0][0]

    # sent to user
    update.message.reply_text(response)

def main():

    """
    function to run all necessary functions to run
    """
    load_model()
    # connect to TG
    updater = Updater(token=token, use_context=True)
    
    # create dispatcher and attach CommandHandler and MessageHandler
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(MessageHandler(Filters.text, custom_gobot))
    
    updater.start_polling()
    updater.idle()

"""
    2. Main
"""
# read config and build model
with open(config_path, encoding='utf-8') as f:
    gobot_config = json.load(f)
#gobot = build_model(gobot_config, download=False)

# run app
if __name__ == '__main__':
    main()

"""
    END
"""
