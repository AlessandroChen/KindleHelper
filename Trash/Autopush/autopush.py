import urllib
import smtplib
import os
from Config import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from email import encoders

def main_push(Filename):

    username = config.username
    password = config.password
    sender = username
    receivers = ','.join([config.receiver])
     
    msg = MIMEMultipart()
    msg['Subject'] = '自动推送'
    msg['From'] = sender
    msg['To'] = receivers
     
    puretext = MIMEText('From KindleHelper')
    msg.attach(puretext)
    att = MIMEText(open('%s' % Filename, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"' % Filename
    msg.attach(att)
     
    # mobipart = MIMEApplication(open('%s.mobi' % Filename, 'rb').read(), 'base64', 'utf-8')
    # mobipart.add_header('Content-Disposition', 'attachment', fileFilename='%s.mobi' % Filename)
    # msg.attach(mobipart)

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


def mail(attach):
    text = "From KindleHelper";
    msg = MIMEMultipart()

    username = config.username
    password = config.password
    sender = username
    receivers = ','.join([config.receiver])
     
    msg['Subject'] = 'Convert'
    msg['From'] = sender
    msg['To'] = receivers
     
    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.qq.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(username, config.receiver, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
