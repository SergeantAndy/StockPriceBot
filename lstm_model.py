import yfinance as yf
import numpy as np
import pandas as pd
import datetime
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import yaml
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import Adam


class LSTMModel:
    """
    Клас LSTMModel реалізує модель Long Short-Term Memory (LSTM) для прогнозування курсу валют.

    Атрибути:
        config (dict): Параметри конфігурації, завантажені з файлу 'config.yaml'.

    Методи:
        get_currency_forecast(currency):
            Отримує дані про валюту, підготовлює їх, навчає модель LSTM та генерує прогнози майбутніх цін.

    """

    def __init__(self):
        """
        Ініціалізує об'єкт класу LSTMModel.
        Завантажує параметри конфігурації з файлу 'config.yaml'.
        """
        self.config = yaml.safe_load(open('conf/config.yaml', 'r'))

    def get_currency_forecast(self, currency):
        """
        Отримує дані про валюту, підготовлює їх, навчає модель LSTM та генерує прогнози майбутніх цін.

        Аргументи:
            currency (str): Код валюти, для якої потрібно зробити прогноз.

        Повертає:
            buffer (io.BytesIO): Буфер зображення графіка прогнозованих цін.

        """

        # Отримання даних про валюту за останні три роки
        start_date = datetime.datetime.now() - datetime.timedelta(days=365*3)
        end_date = datetime.datetime.now()
        currency_data = yf.download(currency, start=start_date, end=end_date, progress=False)

        # Підготовка даних
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(currency_data['Close'].values.reshape(-1, 1))

        # Розподіл даних на тренувальну і тестову вибірки
        train_data = scaled_data[:-14]
        test_data = scaled_data[-14:]

        def create_sequences(data, sequence_length):
            """
            Створює послідовності для введення моделі.

            Аргументи:
                data (ndarray): Дані для створення послідовностей.
                sequence_length (int): Довжина послідовності.

            Повертає:
                X (ndarray): Масив послідовностей.
                y (ndarray): Масив відповідних значень.

            """
            X = []
            y = []
            for i in range(len(data) - sequence_length):
                X.append(data[i : i + sequence_length])
                y.append(data[i + sequence_length])
            return np.array(X), np.array(y)

        sequence_length = 7  # Кількість днів для прогнозу
        X_train, y_train = create_sequences(train_data, sequence_length)
        X_test, y_test = create_sequences(test_data, sequence_length)

        model = Sequential()
        model.add(LSTM(128, activation='relu', input_shape=(sequence_length, 1), return_sequences=True))
        model.add(LSTM(128, activation='relu', return_sequences=True))
        model.add(LSTM(64, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer=Adam(learning_rate=0.001), loss=self.config['model_parameters']['loss'])

        # Навчання моделі
        model.fit(X_train, y_train, epochs=self.config['model_parameters']['epochs'],
                  batch_size=self.config['model_parameters']['batch_size'],
                  verbose=self.config['model_parameters']['verbose'])

        # Прогноз на майбутнє
        future_predictions = []
        last_sequence = X_test[-1]

        for _ in range(14):  # Прогноз на два тижні
            prediction = model.predict(last_sequence.reshape(1, sequence_length, 1))
            future_predictions.append(prediction)
            last_sequence = np.append(last_sequence[1:], prediction)

        future_predictions = np.array(future_predictions).reshape(-1, 1)
        future_predictions = scaler.inverse_transform(future_predictions)

        # Побудова графіка
        plt.figure(figsize=(20, 10))
        plt.plot(currency_data.index[-30:-13], currency_data['Close'][-30:-13], label='Історична ціна')
        plt.plot(currency_data.index[-14:], currency_data['Close'][-14:], label='Минулий тиждень', linestyle='--', c='orange')

        future_predictions_dates = pd.date_range(start=currency_data.index[-2], periods=15)[1:]
        future_predictions_values = future_predictions

        plt.plot(future_predictions_dates, future_predictions_values, label='Прогноз на два тижні вперед', c='green')

        plt.plot([currency_data.index[-1]] + future_predictions_dates.tolist(),
                 [currency_data['Close'][-1]] + future_predictions_values.flatten().tolist(), c='green')

        plt.xlabel('Дата', fontsize=14)
        plt.ylabel('Ціна', fontsize=14)
        plt.title(f'{currency} Прогноз валюти', fontsize=16)
        plt.legend(fontsize=14)
        plt.grid(True, alpha=0.5)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return buffer