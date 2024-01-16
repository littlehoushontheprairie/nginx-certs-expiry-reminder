from datetime import date, timedelta
import os
import logging
import schedule
import time
from mysql.connector import connect, Error
from smtp import SMTP
from email_templates import EmailTemplates

SCRIPT_RUN_TIME: str = os.environ.get("SCRIPT_RUN_TIME", "06:00")
FROM_EMAIL: str = os.environ.get("FROM_EMAIL", "")
TO_EMAIL: str = os.environ.get("TO_EMAIL", "")
EMAIL_GREETING: str = os.environ.get("EMAIL_GREETING", "")
SMTP_URL: str = os.environ.get("SMTP_URL", "")
SMTP_PORT: str = os.environ.get("SMTP_PORT", "")
SMTP_EMAIL: str = os.environ.get("SMTP_EMAIL", "")
SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD", "")

MYSQL_HOST: str = os.environ.get("MYSQL_HOST", "")
MYSQL_DATABASE: str = os.environ.get("MYSQL_DATABASE", "")
MYSQL_USER: str = os.environ.get("MYSQL_USER", "")
MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD", "")

MYSQL_QUERY: str = "SELECT c.nice_name AS cert_name FROM certificate c LEFT JOIN proxy_host p ON c.id = p.certificate_id WHERE c.is_deleted = 0 AND c.expires_on > '{two_weeks_from_now_a}' AND c.expires_on < '{two_weeks_from_now_b}' AND p.id IS NULL;"

# Enable logging
logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                    level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


def job():
    logging.info("Running job...")
    smtp: SMTP = SMTP(smtp_url=SMTP_URL, smtp_port=SMTP_PORT,
                      smtp_email=SMTP_EMAIL, smtp_password=SMTP_PASSWORD)
    email_templates: EmailTemplates = EmailTemplates()

    try:
        with connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        ) as connection:
            logging.info("Connecting to database...")

            two_weeks_from_now_a: date = date.today() + timedelta(weeks=2)
            two_weeks_from_now_b: date = two_weeks_from_now_a + \
                timedelta(days=1)

            cursor = connection.cursor()
            cursor.execute(MYSQL_QUERY.format(
                two_weeks_from_now_a=two_weeks_from_now_a.isoformat(), two_weeks_from_now_b=two_weeks_from_now_b.isoformat()))

            results = cursor.fetchall()

            if (len(results) > 0):
                subject: str = "{} certs are going to expire in 2 weeks.".format(
                    str(len(results)))
                body: str = email_templates.generate_basic_template(
                    dict(email_greeting=EMAIL_GREETING, certs=email_templates.generate_cert_list(results=results)))
                smtp.send_email(from_email=FROM_EMAIL, to_email=TO_EMAIL,
                                subject=subject, body=body)

                logging.info(subject)

            else:
                logging.info("No certs are going to expire in 2 weeks.")

    except Error as e:
        logging.error("Failed to connect to the database.")
        subject: str = "Database Connection Error"
        body: str = email_templates.generate_error_template(
            dict(email_greeting=EMAIL_GREETING, error_message="An error has occurred."))
        smtp.send_email(from_email=FROM_EMAIL, to_email=TO_EMAIL,
                        subject=subject, body=body)

    logging.info("Job finished.")


schedule.every().day.at(SCRIPT_RUN_TIME).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
