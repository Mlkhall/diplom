from apscheduler.schedulers.background import BackgroundScheduler
from data.data_worker import Data
from sql.sql_lite import SQLite

from visual.dash_board import add_dash


if __name__ == '__main__':

    data = Data()

    scheduler = BackgroundScheduler()

    scheduler.start()
    try:
        scheduler.add_job(data.check_and_send_critical_values, 'interval', seconds=5, id='monitoring')
        scheduler.add_job(data.insert_current_values_to_db, 'interval', seconds=2, id='insert_db')
        add_dash()
    except KeyboardInterrupt:
        scheduler.shutdown()
