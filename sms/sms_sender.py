import os
from requests import get
from dotenv import load_dotenv
from dev.config import translate


class SmsSender:
    def __init__(self):
        self.email = os.environ.get('EMAIL', "mikhail.ch2011@yandex.ru")
        self.__api_key = os.environ.get('SMS_API')
        self.number = os.environ.get('NUMBER', 79258824339)

        self._url_authorization = f'https://{self.email}:{self.__api_key}@gate.smsaero.ru/v2/auth'
        self.status = 1 if get(url=self._url_authorization).status_code == 200 else 0

    def send_message(self, text='Сообщение от Найджела'):
        self._url_sms = f'https://{self.email}:{self.__api_key}@gate.smsaero.ru/v2/sms/send?number={self.number}&text={text}&sign=SMS Aero'
        if self.status:
            answer = get(url=self._url_sms).json()
            if answer['success']:
                return answer['data']['extendStatus']
            else:
                return answer
        else:
            return 'Не авторизировались :('

    @staticmethod
    def sms_pattern(param, value, critical, time_critical):
        delta = value - critical
        text = \
        f"""
        Уважаемая Анастасия Чумакова,
        
        По параметру {translate.get(param, param)} превышение критического значения {value:.2f} на {delta:.2f}!
        Время превышения: {time_critical}.
        
        Ваш умный дом.
        """
        return text


