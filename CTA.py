import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Fill in with your CTA key
key = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
url = 'http://www.ctabustracker.com/bustime/api/v2/getpredictions?key=' + key + '&stpid='

# Email and Password credentials. Your texts will be from this email.
email = 'xxxxxxxxxxx@email.domain'
passwd = 'xxxxxxxxxxxxxxxx'

# sms_gtway is your phone number @ a smtp gateway for your cell provider.
# smtp is the email smtp. For example, gmail is 'smtp.gmail.com'
# The port is specifc to the email domain. For gmail, it is 587
sms_gtway = 'number@smtp.gateway'
smtp = "email.smtp"
port = 587

# collect_data : int (id) -> string 
# Takes the stop id you want and returns a formatted string of due times for
# your bus, or returns a string saying that there are no busses coming if none
# are available. 
def collect_data(id):
    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(email, passwd)
    msg = MIMEMultipart()
    msg['To'] = sms_gtway
    msg['From'] = email
    find = url + str(id) + "&format=json"
    r = requests.get(find)

    r = r.json()

    body = r['bustime-response']
    print()

    if 'prd' in body:
        predictions = body['prd']
        times = []
        due = []
        stop = predictions[0]['stpnm']
        for i in predictions:
            times.append(i['tmstmp'])
            due.append(i['prdctdn'])

        ret = "ID: " + str(id) + "\n" + \
              "Stop: " + stop + "\n" + \
              "Due(min): " + str(due).strip('[ ]')
    else:
        ret = "ID: " + str(id) + "\n" + \
              "No Busses on the Way."

    time = datetime.now().time()

    time = time.strftime("%I:%M %p")

    msg['Subject'] = str(time)

    msg.attach(MIMEText(ret, 'plain'))
    sms = msg.as_string()
    server.sendmail(email, sms_gtway, sms)

    server.quit()
    return ret