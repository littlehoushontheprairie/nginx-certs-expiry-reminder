from datetime import date, timedelta
import os
import logging
import schedule
import time
from mysql.connector import connect, Error, errorcode
from smtp import SMTP, Email, SMTPOptions
from email_templates import EmailTemplates

SCRIPT_RUN_TIME: str = os.environ.get("SCRIPT_RUN_TIME", "06:00")

FROM_NAME: str = os.environ.get("FROM_NAME", "NGINX Certs Expiry Reminder")
FROM_EMAIL: str = os.environ.get("FROM_EMAIL")
TO_NAME: str = os.environ.get("TO_NAME", "")
TO_EMAIL: str = os.environ.get("TO_EMAIL")

SMTP_HOST: str = os.environ.get("SMTP_HOST")
SMTP_PORT: int = int(os.environ.get("SMTP_PORT", 465))
SMTP_USER: str = os.environ.get("SMTP_USER")
SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD")

MYSQL_HOST: str = os.environ.get("MYSQL_HOST")
MYSQL_DATABASE: str = os.environ.get("MYSQL_DATABASE")
MYSQL_USER: str = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD")

MYSQL_QUERY: str = "SELECT c.nice_name AS cert_name FROM certificate c LEFT JOIN proxy_host p ON c.id = p.certificate_id WHERE c.is_deleted = 0 AND c.expires_on > '{two_weeks_from_now_a}' AND c.expires_on < '{two_weeks_from_now_b}' AND p.id IS NULL;"

assert (FROM_EMAIL is None, "FROM_EMAIL is required.")
assert (TO_EMAIL is None, "TO_EMAIL is required.")
assert (SMTP_HOST is None, "SMTP_HOST is required.")
assert (SMTP_USER is None, "SMTP_USER is required.")
assert (SMTP_PASSWORD is None, "SMTP_PASSWORD is required.")
assert (MYSQL_HOST is None, "MYSQL_HOST is required.")
assert (MYSQL_DATABASE is None, "MYSQL_DATABASE is required.")
assert (MYSQL_USER is None, "MYSQL_USER is required.")
assert (MYSQL_PASSWORD is None, "MYSQL_PASSWORD is required.")

# Enable logging
logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                    level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


def job():
    logging.info("Running job...")
    smtp_options = SMTPOptions(
        host=SMTP_HOST, port=SMTP_PORT, username=SMTP_USER, password=SMTP_PASSWORD)
    smtp: SMTP = SMTP(smtp_options=smtp_options)
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
                email: Email = Email(
                    from_name=FROM_NAME, from_email=FROM_EMAIL, to_name=TO_NAME, to_email=TO_EMAIL,
                    subject=f"{str(len(results))} certs are going to expire in 2 weeks.",
                    body=email_templates.generate_basic_template(
                        dict(to_name=TO_NAME, certs=email_templates.generate_cert_list(results=results))))
                smtp.send_email(email=email)

                logging.info(
                    f"{str(len(results))} certs are going to expire in 2 weeks.")

            else:
                logging.info("No certs are going to expire in 2 weeks.")

    except Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist")
        else:
            logging.error(error)

        email: Email = Email(
            from_name=FROM_NAME, from_email=FROM_EMAIL, to_name=TO_NAME, to_email=TO_EMAIL,
            subject="Database Connection Error",
            body=email_templates.generate_error_template(
                dict(to_name=TO_NAME, error_message=error)))
        smtp.send_email(email=email)

    logging.info("Job finished.")


schedule.every().day.at(SCRIPT_RUN_TIME).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
