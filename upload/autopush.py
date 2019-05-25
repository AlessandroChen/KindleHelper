# encoding: utf-8
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class emailSender(object):
    def __init__(self):
        self.smtp_host = "smtp.qq.com"      # 发送邮件的smtp服务器（从QQ邮箱中取得）
        self.smtp_port = 465                # smtp服务器SSL端口号，默认是465

    def sendEmailWithAttr(self, kindleEmail, kindleAuthEmail, kindleAuthPwd, filename):
        '''
        发送邮件
        '''
        message = MIMEMultipart()  # 邮件内容，格式，编码
        message['From'] = kindleAuthEmail             # 发件人
        message['To'] = kindleEmail             # 收件人列表
        message['Subject'] = "自动推送"                # 邮件标题
        with open(filename, 'rb') as f:
            attachfile = MIMEApplication(f.read())
        attachfile.add_header('Content-Disposition', 'attachment', filename=filename)
        encoders.encode_base64(attachfile)
        message.attach(attachfile)
        try:
            smtpSSLClient = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)   # 实例化一个SMTP_SSL对象
            loginRes = smtpSSLClient.login(kindleAuthEmail, kindleAuthPwd)      # 登录smtp服务器
            loginRes = (235, b'Authentication successful')
            # print (loginRes);
            if loginRes and loginRes[0] == 235:
                print ("登录成功");
                smtpSSLClient.sendmail(kindleAuthEmail, kindleEmail, message.as_string())
                print ("发送成功")
                return True
            else:
                print ("登陆失败", loginRes[0])
                return False
        except Exception as e:
            print ("发送失败");
            return False
