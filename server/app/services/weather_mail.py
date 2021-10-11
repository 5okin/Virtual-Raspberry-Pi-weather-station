import os
import smtplib
from email.message import EmailMessage


EMAIL_ADDRESS = os.environ['MAILUSER']
EMAIL_PASSWORD= os.environ['MAILPASS']

def send_mail(measurment_temp, latest_measurment_temp, measurment_hum, latest_measurment_hum):
    '''Handles email compose and connection to SMTP'''

    print(f"Email send: {measurment_temp} and {latest_measurment_temp}", flush=True)

    message = f"""The temperature went from {measurment_temp} to {latest_measurment_temp}
                in five minutes, thats a 40% increase! And the air humidity went from 
                {measurment_hum} to {latest_measurment_hum} in five minutes, thats a 50% 
                drop!
                """

    msg = EmailMessage()
    msg['Subject'] = 'Weather Staion Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'nkoutsolelos@gmail.com'

    msg.set_content('This email was send automaticly from the weather server')

    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">Weather is off the charts !!!!</h1>
            <p>{message}</p>
        </body>
    </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
