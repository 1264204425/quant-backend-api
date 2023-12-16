import random
import time
import pandas as pd
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.views import View

from user.models import OkxAccount


#  登录
def login_view(request):
    resp = HttpResponseRedirect('http://localhost:8000/index')
    error_msg = ""
    error_n = None
    if request.method == 'GET':
        # GET返回页面
        return render(request, "user/login.html")
    elif request.method == 'POST':
        # 获取请求参数username和password
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except Exception as e:
            print('--login user error %s' % e)
            error_msg = '用户名或密码错误1'
            return render(request, "user/login.html", locals())

        # 查询email的数据是否存在内置模型User
        if User.objects.filter(email=email):
            login_user = User.objects.get(email=email)
            # print(login_user)
            # 验证账号密码与模型User的账号密码是否一致
            user = authenticate(username=login_user, password=password)
            # 通过验证
            if user:
                error_n = 1
                error_msg = '登陆成功'

                # 记录会话状态
                request.session['email'] = email
                request.session['uid'] = user.id

                login(request, user)
                # return render(request, "user/login.html", locals())
            # username的数据不存在内置模型User
            else:
                error_n = 0
                error_msg = '用户名或密码错误'
                return render(request, "user/login.html", locals())

    if error_n == 1:
        # resp = HttpResponse('http://localhost:8000/index')
        # 记住我
        if 'remember' in request.POST:
            resp.set_cookie('email', email, 3600 * 24)
            resp.set_cookie('uid', user.id, 3600 * 24)

    email = request.POST.get('email')
    # 免登录一天
    user = User.objects.get(email=email)
    login(request, user)
    request.session['email'] = email
    # email = user.email
    # render(request, "user/index.html", locals())
    # return redirect(request,"user/index.html",locals())
    # return render(request, "user/index.html", locals())
    return resp


# def send_sms_code(to_email):
#     """
#     发送邮箱验证码
#     :param to_mail: 发到这个邮箱
#     :return: 成功：0 失败 -1
#     """
#     # 生成邮箱验证码
#     sms_code = '%06d' % random.randint(0, 999999)
#     EMAIL_FROM = "jzh1264204425@163.com"  # 邮箱来自
#     email_title = '邮箱激活'
#     email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
#     send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
#     return send_status, sms_code


# def email_view(self, request):
#     global error_n, send_code
#     if request.method == 'GET':
#         # GET返回页面
#         return render(request, "user/register.html")
#     elif request.method == "POST":
#         error_n = 1
#         send_code = request.POST.get("send_code")
#         email = request.POST.get('email')
#         to_email = email
#         if send_code:
#             send_sms_code(to_email)
#             error_n = 1
#
#     return error_n, send_code
#
#
# def check_code(self, request, send_code):
#     if request.method == 'GET':
#         # GET返回页面
#         return render(request, "user/register.html")
#     elif request.method == "POST":
#         code = request.POST.get('code')
#         if code != send_code:
#             error_n = 0
#             error_msg = '验证码输入错误'
#             return render(request, 'user/register.html', locals())


def register_view(request):
    global user
    sms_code = ""
    error_n = None
    if request.method == 'GET':
        # email = request.POST.get('email')
        # to_email = email
        # send_sms_code(to_email)
        # print(sms_code)
        return render(request, "user/register.html")

    elif request.method == "POST":
        send_code = request.POST.get("send_code")
        code = request.POST.get('code')
        email = request.POST.get('email')
        # to_email = email
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        # send_sms_code(to_email)
        # print(sms_code)
        # if code != sms_code:
        #     error_n = 0
        #     error_msg = '验证码输入错误'
        #     return render(request, 'user/register.html', locals())

        if password_1 != password_2:
            error_n = 0
            error_msg = '两次输入密码不一致'
            return render(request, 'user/register.html', locals())
            # return HttpResponse('两次输入密码不一致')

        # 检查当前用户名称是否可用
        user_name = User.objects.filter(username=username)
        # print(user_name)
        if user_name:
            error_n = 0
            error_msg = '用户名已注册'
            return render(request, 'user/register.html', locals())
            # return HttpResponse('用户名已注册')

        user_email = User.objects.filter(email=email)
        if user_email:
            error_n = 0
            error_msg = '邮箱已注册'
            return render(request, 'user/register.html', locals())

        error_n = 1
        # 插入数据
        try:
            user = User.objects.create_user(username=username, password=password_1, email=email)
        except Exception as e:
            print('--create user error %s' % e)
            error_msg = '用户名已注册'
            return render(request, 'user/register.html', locals())
        # return HttpResponse('注册成功')

        return render(request, "user/register.html", locals())

    return render(request, "user/register.html")


def forgot_view(request):
    error_n = None
    if request.method == 'POST':
        # GET返回页面
        return render(request, "user/forgot.html")
    elif request.method == "GET":
        # send_code = request.POST.get("send_code")
        # code = request.POST.get('code')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        # send_sms_code(to_email)
        # print(sms_code)
        # if code != sms_code:
        #     error_n = 0
        #     error_msg = '验证码输入错误'
        #     return render(request, 'user/register.html', locals())

        if password_1 != password_2:
            error_n = 0
            error_msg = '两次输入密码不一致'
            return render(request, 'user/forgot.html', locals())
            # return HttpResponse('两次输入密码不一致')

        # 检查当前用户名称是否可用
        user_name = User.objects.filter(username=username)
        # print(user_name)
        if user_name is None:
            error_n = 0
            error_msg = '该用户不存在'
            return render(request, 'user/forgot.html', locals())
            # return HttpResponse('用户名已注册')

        user_email = User.objects.filter(email=email)
        if user_email is None:
            error_n = 0
            error_msg = '该邮箱不存在'
            return render(request, 'user/forgot.html', locals())

        error_n = 1
        # 更新数据
        try:
            user = User.objects.update(username=username, password=password_1, email=email)
        except Exception as e:
            print('--updata user error %s' % e)
            error_msg = '密码更改失败'
            return render(request, 'user/forgot.html', locals())
        # return HttpResponse('注册成功')

        # # 免登录一天
        # request.session['username'] = username
        # request.session['uid'] = user.id

    return render(request, "user/forgot.html", locals())


@login_required(login_url='/user/login')
def index_view(request):
    email = request.session.get("email")
    print(email)
    # return redirect("/index")
    return render(request, "user/index.html", locals())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('http://localhost:8000/user/login')


def test_block_view(request):
    # return HttpResponseRedirect('http://localhost:8000/user/block')
    # return HttpResponseRedirect('http://localhost:8000/user/test_block')
    df1 = pd.read_csv('static/data/ahr999.csv')
    day = df1['day']
    # 将时间字符串转换为时间戳
    times = pd.to_datetime(day)
    # 获取年月日信息
    times_ymd = times.dt.strftime("%Y/%m/%d")
    # 将时间放入列表
    date_list = times_ymd.tolist()

    ahr999 = df1['ahr999'].tolist()
    ahr999 = str(ahr999).replace("'", "")
    # list_Data = ahr999.replace("[", "").replace("]", "").split(", ")
    print(date_list)
    print(ahr999)
    # return render(request, 'user/test—block.html')
    return render(request, 'user/test—block.html', locals())


def block_view(request):
    # return HttpResponseRedirect('http://localhost:8000/user/test_block')
    return render(request, 'user/block.html')


@login_required
def ahr999_view(request):
    df1 = pd.read_csv('static/data/ahr999.csv')
    day = df1['day']
    # 将时间字符串转换为时间戳
    times = pd.to_datetime(day)
    # 获取年月日信息
    times_ymd = times.dt.strftime("%Y/%m/%d")
    # 将时间放入列表
    date_list = times_ymd.tolist()

    ahr999 = df1['ahr999'].tolist()
    ahr999 = str(ahr999).replace("'", "")
    print(date_list)
    print(ahr999)
    return render(request, 'user/ahr999.html', locals())


@login_required
def addokxaccount_view(request):
    email = request.user.email
    if request.method == 'GET':
        # GET返回页面
        return render(request, "account/index.html", locals())
    if request.method == 'POST':
        api_key = request.POST.get('okxApiKey')
        api_secret = request.POST.get('okxApiSecret')
        api_password = request.POST.get('okxApiPassword')
        print(api_key, api_secret, api_password)
        email = request.user
        account = OkxAccount(apiKey=api_key, apiSecret=api_secret, apiPassword=api_password, email=email)
        account.save()
        return HttpResponse('success')
        # return HttpResponseRedirect('/accounts/list/')  # 重定向到账户列表页面
    else:
        return HttpResponse('fail')
