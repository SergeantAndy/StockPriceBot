import telebot
import yaml
from src.model import Model
from src.view import View
from src.presenter import Presenter

def load_config():
    with open("conf/config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    return config

def main():
    config = load_config()
    bot = telebot.TeleBot(config['bot']['bot_id'])
    view = View(bot, config)
    model = Model(config)
    presenter = Presenter(bot, view, model)

    @bot.message_handler(commands=['start'])
    def handle_start_command(message):
        presenter.handle_start_command(message)

    @bot.message_handler(func=lambda message: message.text == 'Додати валюту')
    def handle_add_currency_command(message):
        presenter.handle_add_currency_command(message)

    @bot.message_handler(func=lambda message: message.text == 'Видалити валюту')
    def handle_remove_currency_command(message):
        presenter.handle_remove_currency_command(message)

    @bot.message_handler(func=lambda message: message.text == 'Оновити кількість')
    def handle_update_quantity_command(message):
        presenter.handle_update_quantity_command(message)

    @bot.message_handler(func=lambda message: message.text == 'Прогноз')
    def handle_forecast_command(message):
        presenter.handle_forecast_command(message)

    @bot.message_handler(func=lambda message: message.text == 'Показати всі валюти')
    def handle_show_all_currencies_command(message):
        presenter.handle_show_all_currencies_command(message)

    @bot.message_handler(func=lambda message: message.text == 'Допомога')
    def handle_message(message):
        presenter.handle_help_command(message)

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        presenter.handle_unknown_command(message)

    bot.polling()
    model.cursor.close()

if __name__ == '__main__':
    main()
