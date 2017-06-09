# coding=utf-8
__author__ = 'yyx'
__date__ = '2017/5/31 15:53'
from django import forms
from captcha.fields import CaptchaField


# forms.Form对注册表单的一种验证
# 注意foems中的名字要和页面里input的name对应上

# 用来规定user格式
class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # required=True 检验是否为空
    password = forms.CharField(required=True, min_length=5)  # min_length=5 最小字段为5


# 注册效验
class RegisterFrom(forms.Form):
    email = forms.EmailField(required=True)  # 当前端传过来email时，EmailField就会对email进行验证，email必须符合邮箱的正则表达式
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})  # 验证码自定义报错


# 找回密码
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)  # 当前端传过来email时，EmailField就会对email进行验证，email必须符合邮箱的正则表达式
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})  # 验证码自定义报错


class ModifyPwdFrom(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
