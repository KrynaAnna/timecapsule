import os
import time
from datetime import datetime

import pandas as pd
import pytz

from mail import Mail


# Define the target date and current date
date_yesterday = datetime.strptime('2022-11-03', '%Y-%m-%d').date()
date_today = datetime.now(pytz.timezone('Canada/Eastern')).date()

# Define paths
current_dir = os.path.abspath(os.path.dirname(__file__))
instance_folder = os.path.join(current_dir, 'instance')
db_file_path = os.path.join(instance_folder, 'data.db')

# Load data from the database table
database = pd.read_sql_table('data', f"sqlite:///{db_file_path}")

# Main loop to process scheduled emails
while date_today != date_yesterday:
    for i in range(len(database)):
        if database['date_future'][i].date() == date_today:
            # Prepare email parameters
            email_params = {
                "to": database['recipient'][i],
                "sender": "capsule.in.future@gmail.com",
                "subject": f"Capsule time",
                "msg_html": f'''
                    <html>
                    <head>
                        <title>Your Beautiful Email</title>
                    </head>
                    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: white;">
                        <table align="center" border="0" cellpadding="0" cellspacing="0" width="800" style="background-color: #EEF0FCFF; margin-top: 20px;">
                            <tr>
                                <td align="center" style="padding: 40px 0;">
                                    <h1 style="color: rgba(4,15,65,0.74);">Hello {database['name'][i]}!</h1>
                                    <p style="color: #333333; font-size: 18px;">This your letter from past {database['date_past'][i].date()}!</p>
                                    <p style="color: #333333; font-size: 18px;">{database['body'][i]}</p>
                                    <a href="http://localhost:63342/" style="display: inline-block; margin-top: 30px; background-color: rgba(4,15,65,0.74); color: #ffffff; font-size: 20px; text-decoration: none; padding: 10px 20px; border-radius: 5px;">Write new letter</a>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 40px 0; color: #777777; font-size: 16px;">
                                    <p>Need help? Contact our 
                                        <a href="mailto:capsule.in.future@gmail.com">support team</a>!
                                    </p>
                                    <p>Best regards,</p>
                                    <p><b>CAPSULE</b></p>
                                </td>
                            </tr>
                        </table>
                    </body>
                    </html>        
                    ''',
                "signature": False
            }

            # Attach image if available
            if database['img_url'][i] is not None:
                email_params["attachments"] = [
                    f"static/customer/{database['img_url'][i]}"]

            # Create Mail instance and send the message
            mail = Mail(params=email_params)
            mail.send_message()

    # Update date for the next iteration
    date_yesterday = date_today

    # Sleep for 12 hours before the next iteration
    time.sleep(43200)
