from abc import ABC, abstractmethod

class BasePresenter(ABC):
    @abstractmethod
    def handle_start_command(self, message):
        pass
    
    @abstractmethod
    def handle_add_currency_command(self, message):
        pass

    @abstractmethod
    def handle_remove_currency_command(self,message):
        pass

    @abstractmethod
    def handle_update_quantity_command(self, message):
        pass
    
    @abstractmethod
    def handle_forecast_command(self, message):
        pass
    
    @abstractmethod
    def handle_show_all_currencies_command(self, message):
        pass
    
    @abstractmethod
    def handle_unknown_command(self, message):
        pass
    
    @abstractmethod
    def handle_help_command(self,message):
        pass