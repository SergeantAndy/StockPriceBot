from telebot import types
from src.abstract.base_view import BaseView

class View(BaseView):
    def __init__(
            self, 
            bot, 
            config
        ):
        """
        Ініціалізує об'єкт View.

        Параметри:
            bot: Об'єкт бота для взаємодії з Telegram.
            config (dict): Конфігураційний словник з параметрами.
        """
        self.bot = bot
        self.config = config

    def start(
            self, 
            message, 
            currencies_message
        ):
        """
        Початкове повідомлення бота.

        Параметри:
            message: Повідомлення від користувача.
            currencies_message (str): Повідомлення зі списком валют користувача.
        """
        # Створення кнопок
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = types.KeyboardButton('Додати валюту')
        button2 = types.KeyboardButton('Видалити валюту')
        button3 = types.KeyboardButton('Оновити кількість')
        button4 = types.KeyboardButton('Прогноз')
        button5 = types.KeyboardButton('Показати всі валюти')
        button6 = types.KeyboardButton('Допомога')
        keyboard.add(button1, button2, button3, button4, button5, button6)

        self.bot.reply_to(
            message, 
            f"Привіт! Цей бот створений для керування валютами. {currencies_message}",
            reply_markup=keyboard
        )

    def add_currency(
            self, 
            message
        ):
        """
        Повідомлення для введення назви валюти, яку користувач хоче додати.

        Параметри:
            message: Повідомлення від користувача.
        """
        self.bot.reply_to(message, "Введіть назву валюти:")

    def process_currency_quantity(
            self, 
            message
        ):
        """
        Повідомлення для введення кількості валюти, яку користувач хоче додати.

        Параметри:
            message: Повідомлення від користувача.
        """
        self.bot.reply_to(message, "Введіть кількість:")

    def remove_currency(
            self, 
            message
        ):
        """
        Повідомлення для введення назви валюти, яку користувач хоче видалити.

        Параметри:
            message: Повідомлення від користувача.
        """
        self.bot.reply_to(message, "Введіть назву валюти, котру хочете видалити:")

    def process_update_quantity_currency(
            self, 
            message
        ):
        """
        Повідомлення для введення назви валюти, кількість якої користувач хоче оновити.

        Параметри:
            message: Повідомлення від користувача.
        """
        self.bot.reply_to(message, "Введіть назву валюти, котру хочете оновити:")

    def process_update_quantity(
            self, 
            message
        ):
        """
        Повідомлення для введення нової кількості валюти, яку користувач хоче оновити.

        Параметри:
            message: Повідомлення від користувача.
        """
        self.bot.reply_to(message, "Введіть нову кількість:")

    def forecast(
            self, 
            message
        ):
        """
        Повідомлення для введення назви валюти, для якої користувач хоче отримати прогноз.

        Параметри:
            message: Повідомлення від користувача.
        """
        self.bot.reply_to(message, "Введіть назву валюти:")

    def process_currency_input(
            self, 
            chat_id
        ):
        """
        Повідомлення про очікування під час прогнозування валюти.

        Параметри:
            chat_id: Ідентифікатор чату користувача.
        """
        self.bot.send_message(
            chat_id,
            text='Прогнозування займе трошки часу. Зачекайте ...'
        )

    def send_currency_forecast(
            self, 
            chat_id, 
            graph_buffer, 
            currency
        ):
        """
        Надсилає прогноз курсу валюти у форматі фотографії.

        Параметри:
            chat_id: Ідентифікатор чату користувача.
            graph_buffer: Буфер зображення графіка прогнозу.
            currency: Назва валюти.
        """
        self.bot.send_photo(
            chat_id=chat_id, 
            photo=graph_buffer,
            caption='Прогноз ціни {} на два тижні вперед'.format(currency)
        )

    def show_all_currencies(
            self, 
            message, 
            currencies_message
        ):
        """
        Показує повідомлення зі списком всіх валют користувача.

        Параметри:
            message: Повідомлення від користувача.
            currencies_message (str): Повідомлення зі списком валют користувача.
        """
        self.bot.reply_to(message, currencies_message)

    def unknown_command(self, message):
        """
        Повідомлення про невідому команду та вказівку користувачеві використовувати кнопки.

        Параметри:
            message: Повідомлення від користувача.
        """
        self.bot.reply_to(message, "Невідома команда. Скористуйтеся кнопками для взаємодії.")


    def help_command(self, message, userid):
        help_text = "Цей бот дозволяє керувати валютами.\n\n" \
                    "Ви можете використовувати наступні команди та кнопки:\n" \
                    "Кнопка 'Старт' - почати взаємодію з ботом\n" \
                    "Кнопка 'Додати валюту' - додати нову валюту\n" \
                    "Кнопка 'Видалити валюту' - видалити валюту\n" \
                    "Кнопка 'Оновити кількість' - оновити кількість валюти\n" \
                    "Кнопка 'Прогноз' - отримати прогноз ціни валюти\n" \
                    "Кнопка 'Показати всі валюти' - показати всі валюти\n\n" \
                    "Кнопка 'Допомога' - отримати інформацію як користуватися ботом\n\n" \
                    "Будь ласка, користуйтесь кнопками для зручності взаємодії з ботом."

        self.bot.reply_to(message, help_text)
        self.bot.send_message(
            chat_id=userid,
            text = "Цей бот отримує інформацію про валюти, акції і цінні метали з біржі yfinance.\n\n" \
                    "Щоб додавати, оновлювати та видаляти валюти, вам потрібно знати їх абревіатуру (наприклад, BTC-USD)\n\n"\
                    "Для того, щоб отримати назву валюти, перейдіть за посиланням: https://finance.yahoo.com/"
        )   
        self.bot.send_message(
            chat_id = userid,
            text = "Перейдіть до будь-якої валюти і ви побачите її назву у дужках, наприклад, (BTC-USD)"
        )