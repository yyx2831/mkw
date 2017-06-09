# coding=utf-8
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from users.forms import LoginForm, RegisterFrom, ForgetForm, ModifyPwdFrom
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


# 自定义后台验证方法
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 因为密码不是明文所以使用这个方法加密后对比
                return user
        except Exception as e:
            return None


# 用于获取邮件里的激活码，在url active/后面
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 取到数据库里code=active_code的数据
        if all_records:
            for records in all_records:
                email = records.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True  # 将其激活
                user.save()
            return render(request, "login.html")
        else:
            return render(request, "active_fail.html")


# 用类的方法实现注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterFrom()  # 验证码
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterFrom(request.POST)  # 验证码
        if register_form.is_valid():  # 如果效验通过
            user_name = request.POST.get('email', '')  # 获取账号
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get('password', '')  # 获取密码
            user_profile = UserProfile()  # 创建用户models对象
            user_profile.username = user_name  # 在对象里存入username
            user_profile.email = user_name  # 在对象里存入email
            user_profile.is_active = False  # 把is_active设置为未激活状态，以待用户点击邮箱链接激活
            # 在用户里存入密码,make_password用来加密的，可以用check_password(text, passwd)解密-返回true或false
            user_profile.password = make_password(pass_word)
            user_profile.save()  # 保存对象

            send_register_email(user_name, 'register')  # 向用户邮箱发射验证码
            return render(request, "login.html")  # 如果成功就返回login.html页面
        else:
            return render(request, "register.html", {"register_form": register_form})


# 用类的方法实现登陆
class LoginView(View):  # 通过继承View获得get和post方法
    # GET
    def get(self, request):
        return render(request, 'login.html', {})

    # POST
    def post(self, request):
        login_form = LoginForm(request.POST)  # 获取校验方法
        if login_form.is_valid():  # 效验账号密码是否符合规则
            user_name = request.POST.get('username', '')  # 获取账号
            pass_word = request.POST.get('password', '')  # 获取密码
            user = authenticate(username=user_name, password=pass_word)  # 认证，是否和数据库里的账号密码相同
            if user is not None:  # 如果通过认证 user不为空就
                if user.is_active:  # 判断是否激活
                    login(request, user)  # 登陆
                    return render(request, 'index.html', {})  # 登陆成功返回首页
                else:
                    return render(request, 'login.html', {"msg": "用户名未激活", })  # 登陆失败，返回错误内容
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误", })  # 登陆失败，返回错误内容
        else:
            return render(request, 'login.html',
                          {"msg": "用户名或密码错误", "login_form": login_form})  # 效验 失败 login_form 返回效验错误信息


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()  # Forget表单 验证码
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)  # 传入request
        if forget_form.is_valid():  # 判断传入request是否合法
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):  # active_code是url里后缀加上的乱码
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 取到数据库里code=active_code的数据
        if all_records:
            for records in all_records:
                email = records.email
                return render(request, 'password_reset.html', {'email': email})
            return render(request, "login.html")
        else:
            return render(request, "active_fail.html")


class ModifyOowdView(View):
    def post(self, request):
        modify_form = ModifyPwdFrom(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)  # 加密一下
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})

# 函数的方法实现注册
# 如果是post就表示是账号密码
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html', {})
#         else:
#             return render(request, 'login.html', {"msg": "用户名或密码错误"})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})
