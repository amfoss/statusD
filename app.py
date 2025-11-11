import email
import imaplib
import os
import re
import sched
import smtplib
from datetime import datetime, timedelta

from apscheduler import Scheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

load_dotenv()

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
ROOT_URL = "https://root.amfoss.in/"
USERNAME = os.environ["STATUSD_EMAIL"]
APP_PASSWORD = os.environ["STATUSD_APP_PASSWORD"]
MAILING_LIST = os.environ["STATUSD_MAILING_LIST"]

transport = AIOHTTPTransport(url=ROOT_URL)
gql_client = Client(transport=transport)

status_update_template = """Namah Shivaya,

This is an automatically generated thread for sending your daily status update for today. Please send your status update as a reply to this thread after 06:00 PM and before 05:00 AM.
Remember to mention the work you did today (including relevant non-technical work), the work or goals you plan for tomorrow, and any blockers you are facing. Also, include a proper signature for your update.
A good model for a status update would be:

    Namah Shivaya,

    Done:
        Work done in paragraphs, or descriptive bullet points
    Planned:
        Each plan/goal in Bullet Points
    Blockers: (optional) 
        Mention any blockers you are facing (if any), so others in the club can help you out.
    Hours Worked:  [Hours you worked]

    [ Signature ]

Kindly note that an automated bot is tracking your status update, and generating reports. Failing to send status updates repeatedly shall entail severe actions.

Wishing you a productive day!
"""


def send_status_email():
    today_str = datetime.today().strftime("%d-%m-%Y")

    msg = email.message.EmailMessage()
    msg["Subject"] = f"Status Update [{today_str}]"
    msg["From"] = USERNAME
    msg["To"] = MAILING_LIST
    msg.set_content(status_update_template)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(USERNAME, APP_PASSWORD)
        smtp.send_message(msg)


def update_root(emails, date):
    if not emails:
        print("No emails to update")
        return

    try:
        date_str = date.strftime("%Y-%m-%d")
        mutation = gql(
            """
            mutation MarkStatusUpdate($emails: [String!]!, $date: NaiveDate!) {
                markStatusUpdate(emails: $emails, date: $date) {
                    isSent
                }
            }
        """
        )

        params = {"emails": emails, "date": date_str}
        print(f"Sending GraphQL Mutation with params: {params}")
        result = gql_client.execute(mutation, variable_values=params)
    except Exception as e:
        print(f"Error updating ROOT: {e}")


def fetch_updates():
    M = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    M.login(USERNAME, APP_PASSWORD)

    yesterday = datetime.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%d-%m-%Y")

    M.select("INBOX")
    subj = f"Status Update [{yesterday_str}]"
    status, data = M.search(None, f'(SUBJECT "{subj}")')
    mail_ids = data[0].split()

    emails = []
    for num in mail_ids:
        status, msg_data = M.fetch(num, "(RFC822)")
        if status != "OK":
            print(f"Error fetching mail {num}")
            continue

        raw_msg = msg_data[0][1]
        msg = email.message_from_bytes(raw_msg)["From"]
        match = re.search(r"<(.*?)>", msg)

        if match:
            emails.append(match.group(1))

    update_root(emails, yesterday)

    M.logout()


if __name__ == "__main__":
    scheduler = Scheduler()
    print("StatusD Online!")
    scheduler.add_schedule(fetch_updates, CronTrigger(hour=6, minute=30))
    scheduler.add_schedule(send_status_email, CronTrigger(hour=18))
    scheduler.run_until_stopped()
