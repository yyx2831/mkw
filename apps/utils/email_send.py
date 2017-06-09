# coding=utf-8
__author__ = 'yyx'
__date__ = '2017/6/2 17:02'

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from mkw.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()  # 邮箱验证码models
    code = random_str(16)  # 16位的随机字符串
    email_record.code = code  # 传进来的验证码
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''  # 邮件标题
    email_body = ''  # 邮件正文

    if send_type == 'register':
        email_title = "慕学在线网注册激活链接"
        email_body = "请点解下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # django提供的内部函数，用来发送邮件，发送成功返回true
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "慕学在线网密码重置链接"
        email_body = "请点解下面的链接重置你的账号: http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # django提供的内部函数，用来发送邮件，发送成功返回true
        if send_status:
            pass


# 随机生成一个字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1  # chars长度
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]  # random.randint内用于生成0-length内的随机数
    return str
