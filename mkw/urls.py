# coding=utf-8
"""mkw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView  # TemplateView可以不用自己写跳转view也可以完成跳转
from apps.users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyOowdView
import xadmin

# TemplateView自带的view不用自己写跳转view也可以完成跳转
urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name="index.html"), name='index'),  # 使用django自带的TemplateView做跳转
    # url('^login/$', LoginView, name='login'),     # 自己写的跳转
    url('^login/$', LoginView.as_view(), name='login'),  # 登陆
    url('^register/$', RegisterView.as_view(), name='register'),  # 注册
    url(r'^captcha/', include('captcha.urls')),  # 验证码
    # 邮箱激活,解析出url aactive 后面为了验证生成的乱码, 这里<>可以随意写后面要用这个名字调用, 使用正则表达式解析的
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyOowdView.as_view(), name='modify_pwd'),
]
