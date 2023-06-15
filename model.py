import mysql.connector
import yfinance as yf
from src.lstm_model import LSTMModel
from src.abstract.base_model import BaseModel

class Model(BaseModel):
    def __init__(self, config):
        """
        Ініціалізує об'єкт Model.

        Параметри:
            config (dict): Конфігураційний словник з параметрами підключення до бази даних.

        Атрибути:
            config (dict): Конфігураційний словник з параметрами підключення до бази даних.
            db (mysql.connector.connection.MySQLConnection): Об'єкт підключення до бази даних.
            cursor (mysql.connector.cursor.MySQLCursor): Об'єкт курсора для виконання запитів до бази даних.
        """
        self.config = config

        # Підключення до бази даних
        self.db = mysql.connector.connect(
            host=self.config['sql_parameters']['host'],
            user=self.config['sql_parameters']['user'],
            password=self.config['sql_parameters']['password'],
            database=self.config['sql_parameters']['database']
        )

        self.cursor = self.db.cursor()

    def show_currencies(
            self, 
            user_id
        ):
        """
        Показує валюти користувача разом з їхніми кількостями і цінами.

        Параметри:
            user_id (int): Ідентифікатор користувача.

        Повертає:
            str: Повідомлення зі списком валют користувача та їхніми деталями.
        """
        self.cursor.execute(
            "SELECT currency_name, quantity FROM `users-currencies` WHERE userid = %s", 
            (user_id,)
        )
        result = self.cursor.fetchall()

        if result:
            message = "Ваші валюти:\n"
            for row in result:
                currency_name, quantity = row
                currency_price = round(self.__get_currency_price(currency_name), 2)
                if currency_price is not None:
                    currency_price_usd = round(float(currency_price) * float(quantity), 2)
                    message += f"- {currency_name}: \n     Кількість: {quantity} \n     Ціна: {currency_price_usd} USD \n     Ціна за штуку: {currency_price} USD\n\n"
                else:
                    message += f"- {currency_name}: \n     Кількість: {quantity} \n     Ціна: недоступно \n     Ціна за штуку: недоступно\n\n"
        else:
            message = "У вас нема збережених валют."

        return message

    def __get_currency_price(
            self, 
            currency_symbol
        ):
        """
        Отримує ціну валюти за символом.

        Параметри:
            currency_symbol (str): Символ валюти.

        Повертає:
            float: Ціна валюти за символом.
        """
        ticker_yahoo = yf.Ticker(currency_symbol)
        data = ticker_yahoo.history()
        last_quote = data['Close'].iloc[-1]

        return last_quote

    def add_currency(
            self, 
            user_id, 
            currency_name, 
            quantity
        ):
        """
        Додає нову валюту користувачу.

        Параметри:
            user_id (int): Ідентифікатор користувача.
            currency_name (str): Назва валюти.
            quantity (float): Кількість валюти.
        """
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO `users-currencies` (userid, currency_name, quantity) VALUES (%s, %s, %s)",
            (user_id, currency_name, quantity)
        )
        self.db.commit()
        
    def remove_currency(
            self, 
            user_id, 
            currency_name
        ):
        """
        Видаляє валюту користувача.

        Параметри:
            user_id (int): Ідентифікатор користувача.
            currency_name (str): Назва валюти.

        Повертає:
            int: Кількість видалених записів.
        """
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM `users-currencies` WHERE userid = %s AND currency_name = %s",
            (user_id, currency_name)
        )
        self.db.commit()
        deleted_count = cursor.rowcount
        
        return deleted_count

    def update_quantity(
            self, 
            user_id, 
            currency_name, 
            quantity
        ):
        """
        Оновлює кількість валюти користувача.

        Параметри:
            user_id (int): Ідентифікатор користувача.
            currency_name (str): Назва валюти.
            quantity (float): Нова кількість валюти.

        Повертає:
            int: Кількість оновлених записів.
        """
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE `users-currencies` SET quantity = %s WHERE userid = %s AND currency_name = %s",
            (quantity, user_id, currency_name)
        )
        self.db.commit()
        updated_count = cursor.rowcount
        
        return updated_count

    def get_currency_forecast(
            self, 
            currency
        ):
        """
        Отримує прогноз курсу валюти.

        Параметри:
            currency (str): Символ валюти.

        Повертає:
            graph_buffer (bytes): Зображення графіка прогнозу курсу валюти.
        """
        lstm_model = LSTMModel()
        graph_buffer = lstm_model.get_currency_forecast(currency)
        return graph_buffer