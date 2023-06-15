from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def show_currencies(self, user_id):
        pass

    @abstractmethod
    def add_currency(self, user_id, currency_name, quantity):
        pass

    @abstractmethod
    def remove_currency(self, user_id, currency_name):
        pass

    @abstractmethod
    def update_quantity(self, user_id, currency_name, quantity):
        pass

    @abstractmethod
    def get_currency_forecast(self, currency):
        pass