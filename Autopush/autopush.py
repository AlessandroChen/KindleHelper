import urllib
import smtplib
from Config import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def main_push(Filename):
    username = config.username
    password = config.password
    sender = username
    receivers = ','.join([config.receiver])
     
    msg = MIMEMultipart()
    msg['Subject'] = ''
    msg['From'] = sender
    msg['To'] = receivers
     
    puretext = MIMEText('')
    msg.attach(puretext)
     
    mobipart = MIMEApplication(open('%s.mobi' % Filename, 'rb').read())
    mobipart.add_header('Content-Disposition', 'attachment', fileFilename='%s.mobi' % Filename)
    msg.attach(mobipart)

    try:
      client = smtplib.SMTP()
      client.connect('smtp.qq.com')
      client.login(username, password)
      client.sendmail(sender, receivers, msg.as_string())
      client.quit()
      print ('发送成功！')
    except smtplib.SMTPRecipientsRefused:
      print ('Recipient refused')
    except smtplib.SMTPAuthenticationError:
      print ('Auth error')
    except smtplib.SMTPSenderRefused:
      print ('Sender refused')
