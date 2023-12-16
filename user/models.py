from django.db import models
from django.http import HttpResponse
# Django内置的用户认证系统中提供的User模型。它包含了一些常见的用户认证相关的属性，例如用户名、密码、电子邮件等。
# 在Django应用程序中需要用户认证时，通常会使用User模型来实现.
from django.contrib.auth.models import User


# Create your models here.


# def index(request):
#     user = User.objects.create_user(username='xujin', email='qq@qq.com', password='111111')
#     return HttpResponse('success')

# okx api
class OkxAccount(models.Model):
    # id = models.AutoField(primary_key=True)
    apiKey = models.CharField(max_length=100)
    apiSecret = models.CharField(max_length=100)
    apiPassword = models.CharField(max_length=100)
    email = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ['id']

# binance api
class BinanceAccount(models.Model):
    # id = models.AutoField(primary_key=True)
    apiKey = models.CharField(max_length=100)
    apiPassword = models.CharField(max_length=100)
    email = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ['id']

