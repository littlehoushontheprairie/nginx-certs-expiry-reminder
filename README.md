# NGINX Certs Expiry Reminder

Need something that notifies you when a manual NGINX cert expires? This script will check the NGINX schema for expiries and notify you when one is found if it is about to expire within 2 weeks via email.

## Setup

#### Running Locally

1. Download repo
    - `git clone https://github.com/littlehoushontheprairie/nginx-certs-expiry-reminder.git`
    - `git checkout develop`
    - `git pull`
    - `cd nginx-certs-expiry-reminder`
2. Export environment variables
3. Run
    - `python3 nginx_certs_expiry_reminder.py`

#### Building and Running as Container from Source

1. Download repo
    - `git checkout develop`
    - `git pull`
    - `cd nginx-certs-expiry-reminder`
2. Export environment variables
3. run docker-compose
    - `docker-compose up --build -d`

#### Running Container from GitHub Docker Registry (using Terminal)

1. Download `latest` container
    - `docker pull ghcr.io/littlehoushontheprairie/nginx-certs-expiry-reminder:latest`
2. Run container
    - ```
      docker run --restart=always -d --network host \
      --name nginx_certs_expiry_reminder \
      -e TZ="America/Los_Angeles" \
      -e FROM_EMAIL="from@example.com" \
      -e TO_EMAIL="to@example.com" \
      -e SMTP_HOST="smtp.example.com" \
      -e SMTP_USER="laura@example.com" \
      -e SMTP_PASSWORD="8f5cd6729h0v5d247vc190ddcs4l2a" \
      -e MYSQL_HOST=" mysql.example.com" \
      -e MYSQL_DATABASE="nginx_proxy_manager" \
      -e MYSQL_USER="mysql_nginx_user" \
      -e MYSQL_PASSWORD="8f5cd6729h0v5d247vc190ddcs4l2b" \
      ghcr.io/littlehoushontheprairie/nginx-certs-expiry-reminder:latest
      ```

#### Running Container from GitHub Docker Registry (using docker-compose)

1. Create `docker-compose.yml` file
2. Add content.

    - ```
      version: "3.5"

      services:
          nginx_certs_expiry_reminder:
              container_name: nginx_certs_expiry_reminder
              image: ghcr.io/littlehoushontheprairie/nginx_certs_expiry_reminder:latest
              restart: always
              network_mode: host
              environment:
                  TZ: America/Los_Angeles
                  FROM_EMAIL: "${FROM_EMAIL}"
                  TO_EMAIL: "${TO_EMAIL}"
                  SMTP_HOST: "${SMTP_HOST}"
                  SMTP_USER: "${SMTP_USER}"
                  SMTP_PASSWORD: "${SMTP_PASSWORD}"
                  MYSQL_HOST: "${MYSQL_HOST}"
                  MYSQL_USER: "${MYSQL_USER}"
                  MYSQL_PASSWORD: "${MYSQL_PASSWORD}"
                  MYSQL_DATABASE: "${MYSQL_DATABASE}"
      ```

3. Export environment variables
4. Run `docker-compose up -d`

## Email Templates

The script reads in email templates everytime it is ran. You can customize the templates located in the _templates_ folder. They are read in as HTML files and are injected at runtime with the information.

### Structure

-   error.html - Error Template
-   index.html - Main Template

## Environment Variables

| Variable        | Required | Default                     | Example                        | Needed by                     |
| --------------- | -------- | --------------------------- | ------------------------------ | ----------------------------- |
| SCRIPT_RUN_TIME | false    | 06:00                       | 00:00 - 23:59                  | Scheduler                     |
| FROM_NAME       | false    | NGINX Certs Expiry Reminder | NGINX Certs Expiry Reminder    | SMTP Server (send email from) |
| FROM_EMAIL      | true     | ---                         | from@example.com               | SMTP Server (send email from) |
| TO_NAME         | false    |                             |                                | SMTP Server (send email to)   |
| TO_EMAIL        | true     | ---                         | to@example.com                 | SMTP Server (send email to)   |
| SMTP_HOST       | true     | ---                         | smtp.example.com               | SMTP Server                   |
| SMTP_PORT       | false    | 465                         | 465                            | SMTP Server                   |
| SMTP_USER       | true     | ---                         | laura@example.com              | SMTP Server                   |
| SMTP_PASSWORD   | true     | ---                         | 8f5cd6729h0v5d247vc190ddcs4l2a | SMTP Server                   |
| MYSQL_HOST      | true     | ---                         | mysql.example.com              | MySQL Server                  |
| MYSQL_USER      | true     | ---                         | mysql_nginx_user               | MySQL Server                  |
| MYSQL_PASSWORD  | true     | ---                         | 8f5cd6729h0v5d247vc190ddcs4l2a | MySQL Server                  |
| MYSQL_DATABASE  | true     | ---                         | nginx_proxy_manager            | MySQL Server                  |

**NOTE:** For security purposes, it is strong recommended that you use a generated API passwords.
