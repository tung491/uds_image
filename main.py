from telegram.ext import Updater, CommandHandler
from selenium import webdriver
from urllib.parse import quote
import os

updater = Updater(token=os.getenv('TELEGRAM_TOKEN'), use_context=True)
dispatcher = updater.dispatcher
driver = webdriver.Chrome(executable_path='/Users/tung491/Downloads/chromedriver')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def uds(update, context):
    word = ' '.join(context.args)
    url = f'https://www.urbandictionary.com/define.php?term={quote(word)}'
    driver.get(url)
    def_panels = driver.find_elements_by_xpath('//div[@class="def-panel "]')
    if def_panels:
        def_panels.remove(def_panels[1])
        for def_panel in def_panels:
            for cls in ['row', 'mug-ad', 'def-footer', 'contributor']:
                rm_element = def_panel.find_element_by_class_name(cls)
                driver.execute_script("""
                                        var element = arguments[0];
                                        element.parentNode.removeChild(element);
                                        """, rm_element)
                with open('defination.png', 'wb') as f:
                    f.write(def_panel.screenshot_as_png)
            context.bot.send_photo(update.effective_chat.id, photo=open('defination.png', 'rb'))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='There is no defination for this word')


if __name__ == '__main__':
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    uds_handler = CommandHandler('uds', uds)
    dispatcher.add_handler(uds_handler)
    updater.start_polling()
