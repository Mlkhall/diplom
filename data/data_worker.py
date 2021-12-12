import os
import sqlite3
from serial import SerialException

from typing import Optional, Any
from arduino.arduino_data_reader import Arduino
from sql.sql_lite import SQLite
from sms.sms_sender import SmsSender
from dev.config import critical_values
from data.data_transport import SmartHome


class Data:
    def __init__(self) -> None:
        self.ports = Arduino.get_all_ports()
        self.current_port = os.environ.get('PORT') if self.ports[-1] == os.environ.get('PORT') else self.ports[-1]
        try:
            self._arduino = Arduino(port=self.current_port)
        except SerialException:
            self.status = "нет подключения к порту"
        else:
            self.status = "OK"
            self.current_values = self.get_data_from_sensors()

        self.tb_name = os.environ.get('TABLE_NAME', "smart_home")

        self.critical_values = critical_values

        self.sms = SmsSender()

    def get_data_from_sensors(self) -> Optional[Any]:
        if self.status == "OK":
            return self._arduino.get_data_from_arduino()
        else:
            return print(f"ERROR: {self.status}")

    def check_and_send_critical_values(self):
        print("Проверяем значения.")
        if self.status == "OK":
            self.current_values = self.get_data_from_sensors()
            for parameter in self.critical_values:
                if self.current_values[parameter] > self.critical_values[parameter]:
                    mess = self.sms.sms_pattern(param=parameter,
                                                value=self.current_values[parameter],
                                                critical=self.critical_values[parameter],
                                                time_critical=self.current_values['date']
                                                )

                    self.sms.send_message(text=mess)
        else:
            return print(f"ERROR: {self.status}")

    def insert_current_values_to_db(self):
        if self.status == "OK":
            with sqlite3.connect('db/smart_home.db') as sqlite_conn:
                self.sql_lite = SQLite(sqlite_cursor=sqlite_conn.cursor(), sqlite_connect=sqlite_conn)
                try:
                    smart_home_data = SmartHome(**self.current_values)
                    self.sql_lite.insert_value(data=smart_home_data, tb_name="smart_home")
                except TypeError:
                    return print("ERROR: BAD DATA")
                else:
                    return print('INFO: Записано значение!')
        else:
            return print(f"ERROR: {self.status}")

    def get_data_from_db_by_col_name(self):
        with sqlite3.connect('db/smart_home.db') as sqlite_conn:
            self.sql_lite = SQLite(sqlite_cursor=sqlite_conn.cursor(), sqlite_connect=sqlite_conn)

            return self.sql_lite.get_values_from_column()




