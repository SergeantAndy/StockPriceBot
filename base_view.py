from abc import ABC, abstractmethod

class BaseView(ABC):
    @abstractmethod
    def start(self, message, currencies_message):
        pass

    @abstractmethod
    def add_currency(self, message):
        pass

    @abstractmethod
    def process_currency_quantity(self, message):
        pass

    @abstractmethod
    def remove_currency(self, message):
        pass

    @abstractmethod
    def process_update_quantity_currency(self, message):
        pass

    @abstractmethod
    def process_update_quantity(self, message):
        pass

    @abstractmethod
    def forecast(self, message):
        pass

    @abstractmethod
    def process_currency_input(self, chat_id):
        pass

    @abstractmethod
    def send_currency_forecast(self, chat_id, graph_buffer, currency):
        pass

    @abstractmethod
    def show_all_currencies(self, message, currencies_message):
        pass
    
    @abstractmethod
    def unknown_command(self, message):
        pass

    @abstractmethod
    def help_command(self, message, userid):
        pass