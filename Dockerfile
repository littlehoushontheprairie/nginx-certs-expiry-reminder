FROM python:latest

WORKDIR /usr/src/app

COPY nginx_certs_expiry_reminder.py .
COPY smtp.py .
COPY email_templates.py .
COPY templates/index.html ./templates/index.html
COPY templates/error.html ./templates/error.html
RUN chmod 0755 nginx_certs_expiry_reminder.py smtp.py email_templates.py templates/index.html templates/error.html 
RUN pip install schedule mysql-connector-python

CMD [ "python", "./nginx_certs_expiry_reminder.py" ]
