import yfinance as yf
from src.abstract.base_presenter import BasePresenter


class Presenter(BasePresenter):
    def __init__(
            self, 
            bot, 
            view, 
            model
        ):
        """
        Ініціалізує об'єкт Presenter.

        Параметри:
            bot: Об'єкт Telegram-бота.
            view: Об'єкт View для відображення повідомлень користувачеві.
            model: Об'єкт Model для обробки даних.
        """
        self.bot = bot
        self.view = view
        self.model = model

    def handle_start_command(
            self, 
            message
        ):
        """
        Обробляє команду /start.

        Відображає початкове повідомлення та список валют користувача.

        Параметри:
            message: Повідомлення від користувача.
        """
        user_id = message.from_user.id
        currencies_message = self.model.show_currencies(user_id)
        self.view.start(message, currencies_message)

    #### Додавання валют
    def handle_add_currency_command(
            self, 
            message
        ):
        """
        Обробляє команду "Додати валюту".

        Відображає повідомлення для введення назви валюти.

        Параметри:
            message: Повідомлення від користувача.
        """
        user_id = message.from_user.id
        self.view.add_currency(message)
        self.bot.register_next_step_handler(message, self.handle_process_currency_name, user_id)

    def handle_process_currency_name(
            self, 
            message, 
            user_id
        ):
        """
        Обробляє введену користувачем назву валюти.

        Перевіряє, чи існує валюта з введеною назвою. Якщо так, відображає повідомлення для введення кількості валюти.

        Параметри:
            message: Повідомлення від користувача.
            user_id: Ідентифікатор користувача.
        """
        currency_name = message.text
        ticker = yf.Ticker(currency_name)
        if not ticker.info:
            self.view.bot.reply_to(message, "Дана валюта не існує")
            return
        self.view.process_currency_quantity(message)
        self.bot.register_next_step_handler(
            message, 
            self.handle_process_currency_quantity, 
            user_id, 
            currency_name
        )

    def handle_process_currency_quantity(
            self, 
            message, 
            user_id, 
            currency_name
        ):
        """
        Обробляє введену користувачем кількість валюти.

        Додає валюту до списку користувача з введеною назвою та кількістю.

        Параметри:
            message: Повідомлення від користувача.
            user_id: Ідентифікатор користувача.
            currency_name: Назва валюти.
        """
        quantity = message.text
        self.model.add_currency(
            user_id, 
            currency_name, 
            quantity
        )
        self.view.bot.reply_to(message, "Валюта успішно додана")
    ### /додавання валют

    ### видалення валюти
    def handle_remove_currency_command(
            self, 
            message
        ):
        """
        Обробляє команду "Видалити валюту".

        Відображає повідомлення для введення назви валюти, яку користувач бажає видалити.

        Параметри:
            message: Повідомлення від користувача.
        """
        user_id = message.from_user.id
        self.view.remove_currency(message)
        self.bot.register_next_step_handler(
            message, 
            self.handle_process_remove_currency, 
            user_id
        )

    def handle_process_remove_currency(self, message, user_id):
        """
        Обробляє введену користувачем назву валюти для видалення.

        Видаляє валюту зі списку користувача з введеною назвою.

        Параметри:
            message: Повідомлення від користувача.
            user_id: Ідентифікатор користувача.
        """
        currency_name = message.text
        deleted = self.model.remove_currency(user_id, currency_name)
        if deleted == 0:
            self.view.bot.reply_to(message, "У вас немає такої валюти")
        else:
            self.view.bot.reply_to(message, "Валюта успішно видалена")
    ### /видалення валюти

    ### Оновлення валюти
    def handle_update_quantity_command(
            self, 
            message
        ):
        """
        Обробляє команду "Оновити кількість".

        Відображає повідомлення для введення назви валюти, для якої користувач бажає оновити кількість.

        Параметри:
            message: Повідомлення від користувача.
        """
        user_id = message.from_user.id
        self.view.process_update_quantity_currency(message)
        self.bot.register_next_step_handler(
            message, 
            self.handle_process_update_quantity_currency, 
            user_id
        )

    def handle_process_update_quantity_currency(self, message, user_id):
        """
        Обробляє введену користувачем назву валюти для оновлення кількості.

        Перевіряє, чи валюта з введеною назвою присутня у списку користувача.
        Якщо так, відображає повідомлення для введення нової кількості.

        Параметри:
            message: Повідомлення від користувача.
            user_id: Ідентифікатор користувача.
        """
        currency_name = message.text
        self.model.cursor.execute(
            "SELECT * FROM `users-currencies` WHERE userid = %s AND currency_name = %s",
            (user_id, currency_name)
        )
        result = self.model.cursor.fetchall()
        if result:
            self.view.process_update_quantity(message)
            self.bot.register_next_step_handler(
                message, 
                self.handle_process_update_quantity, 
                user_id, 
                currency_name
            )
        else:
            self.view.bot.reply_to(message, "У вас немає такої валюти")
        # self.model.cursor.close()

    def handle_process_update_quantity(
            self, 
            message, 
            user_id, 
            currency_name
        ):
        """
        Обробляє введену користувачем нову кількість валюти для оновлення.

        Оновлює кількість валюти користувача з введеною назвою.

        Параметри:
            message: Повідомлення від користувача.
            user_id: Ідентифікатор користувача.
            currency_name: Назва валюти.
        """
        quantity = message.text
        updated = self.model.update_quantity(
            user_id, 
            currency_name, 
            quantity
        )
        if updated == 0:
            self.view.bot.reply_to(message, "У вас немає такої валюти")
        else:
            self.view.bot.reply_to(message, "Кількість валюти успішно оновлено")
    ### /Оновлення валюти

    ### Прогноз валюти
    def handle_forecast_command(self, message):
        """
        Обробляє команду "Прогноз валюти".

        Відображає повідомлення для введення назви валюти, для якої користувач бажає отримати прогноз.

        Параметри:
            message: Повідомлення від користувача.
        """
        user_id = message.chat.id
        self.view.forecast(message)
        self.bot.register_next_step_handler(
            message, 
            self.handle_process_currency_input, 
            user_id
        )

    def handle_process_currency_input(
            self, 
            message, 
            chat_id
        ):
        """
        Обробляє введену користувачем назву валюти для прогнозу.

        Отримує прогноз для валюти з введеною назвою і відображає його.

        Параметри:
            message: Повідомлення від користувача.
            chat_id: Ідентифікатор чату.
        """
        currency = message.text
        try:
            graph_buffer = self.model.get_currency_forecast(currency)
            self.view.send_currency_forecast(
                chat_id, 
                graph_buffer, 
                currency
            )
        except:
            self.view.bot.send_message(
                chat_id=chat_id,
                text='Виникла помилка при отриманні прогнозу для валюти {}'.format(currency)
            )
    ### /Прогноз валюти


    ### Показати всі валюти
    def handle_show_all_currencies_command(
            self, 
            message
        ):
        """
        Обробляє команду "Показати всі валюти".

        Відображає список всіх валют користувача.

        Параметри:
            message: Повідомлення від користувача.
        """
        user_id = message.from_user.id
        currencies_message = self.model.show_currencies(user_id)
        self.view.show_all_currencies(
            message, 
            currencies_message
        )
    ### /Показати всі валюти
    
    def handle_unknown_command(
            self, 
            message
        ):
        self.view.unknown_command(message)


    def handle_help_command(
            self,
            message
        ):
        user_id = message.chat.id
        self.view.help_command(message, user_id)