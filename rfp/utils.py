import os
import requests

from decouple import config

MAILGUN_API_KEY = config('MAILGUN_API_KEY')
MAILGUN_DOMAIN = config('MAILGUN_DOMAIN')
MAILGUN_FROM_EMAIL = f"Mailgun Sandbox <postmaster@{MAILGUN_DOMAIN}>"

def send_simple_message(to_email, to_name, subject, message):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_FROM_EMAIL,
            "to": f"{to_name} <{to_email}>",
            "subject": subject,
            "text": message
        }
    )
