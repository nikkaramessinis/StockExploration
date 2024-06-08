import yagmail

from config.secrets import GMAIL_ADDRESS, GMAIL_PASSWORD


def send_email(subject, body, to_emails):
    # Email configuration
    yag = yagmail.SMTP(GMAIL_ADDRESS, GMAIL_PASSWORD)

    to_emails = to_emails if isinstance(to_emails, list) else [to_emails]

    try:
        yag.send(to=to_emails, subject=subject, contents=body)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def schedule_email_alert(args):
    enabled = args.get("enabled")
    if not enabled:
        print("Email alerts are disabled.")
        return

    recipients = args.get("recipients")
    if not recipients or recipients == None:
        print("Recipients are required.")
        return

    subject = "Stock Alert"
    body = "MALAKA BUY IT"
    send_email(subject, body, recipients)

    print("Email alert scheduled successfully!")
