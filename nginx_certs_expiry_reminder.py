import os
import logging
import schedule
import time
from mysql.connector import connect, Error
from smtp import SMTP
from email_templates import EmailTemplates

FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')
EMAIL_GREETING = os.environ.get('EMAIL_GREETING')
SMTP_URL = os.environ.get('SMTP_URL')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

# Enable logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def job():
    logging.info('Running job...')
    smtp = SMTP(smtp_url=SMTP_URL, smtp_port=SMTP_PORT,
                smtp_email=SMTP_EMAIL, smtp_password=SMTP_PASSWORD)
    email_templates = EmailTemplates()

    try:
        with connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        ) as connection:
            print(connection)
    except Error as e:
        print(e)

    # TODO Write Script


job()

# schedule.every().day.at('15:00').do(job)

# while True:
#    schedule.run_pending()
#    time.sleep(1)
