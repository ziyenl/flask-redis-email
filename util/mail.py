import requests
import os
from dotenv import load_dotenv


def send_simple_message(to, subject, body, html):
    """
    Send simple email message via mail gun email automation software
    :param to: email
    :param subject: email subject header
    :param body: email body
    :param html: html template
    :return: post request
    """
    load_dotenv()
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = domain = os.getenv("MAILGUN_API_KEY")
    return requests.post(
        "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
        auth=("api", api_key),
        data={"from": f"Admin User <mailgun@{domain}>",
              "to": [to, f"YOU@{domain}"],
              "subject": subject,
              "text": body},
        html=html)