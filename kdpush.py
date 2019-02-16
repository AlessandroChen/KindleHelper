# encoding: utf-8

from Autopush import autopush
from Config import config
from sys import argv

script, filename = argv

mail = autopush.emailSender()

mail.sendEmailWithAttr(config.receiver, config.username, config.password, filename);


