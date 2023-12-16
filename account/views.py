from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from user.models import OkxAccount, BinanceAccount
from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
# okx_api刷新
# def okx_api(request):
#     okx_account_list = OkxAccount.objects.all()
#     okx_account_data = []
#     for okx_account in okx_account_list:
#         okx_account_data.append({
#             # 'id': okx_account.id,
#             'api_key': okx_account.apiKey,
#             'api_secret': okx_account.apiSecret,
#             'api_password': okx_account.apiPassword,
#         })
#     return JsonResponse(okx_account_data, safe=False)

# 删除okx api账户
def delete_okx_account(request):
    email = request.user.email
    email_id = request.user.id
    okx_account = OkxAccount.objects.filter(email_id=email_id)
    # # 通过 account_id 获取要删除的账户
    # okx_account = OkxAccount.objects.get(email_id=email_id)
    okx_account.delete()
    return HttpResponseRedirect('/account/index/')


# 删除binance api账户
def delete_binance_account(request):
    email = request.user.email
    email_id = request.user.id
    binance_account = BinanceAccount.objects.filter(email_id=email_id)
    # # 通过 account_id 获取要删除的账户
    # okx_account = OkxAccount.objects.get(email_id=email_id)
    binance_account.delete()
    return HttpResponseRedirect('/account/index/')


# Django的ORM进行查询，在视图函数中查询该用户对应的所有API信息，然后将结果传递给模板，使用模板语言进行渲染.
def display_okx_accounts(request):
    # 获取当前用户
    email = request.user.email
    # user = request.user
    email_id = request.user.id
    # 查询该用户对应的所有 OkxAccount 记录
    okx_accounts = OkxAccount.objects.filter(email_id=email_id)
    # 将查询结果传递给模板
    context = {'okx_accounts': okx_accounts}
    # print(okx_accounts)
    # return render(request, 'account/test.html', context)
    return render(request, 'account/have_okx.html', context)


def display_binance_accounts(request):
    # 获取当前用户
    email = request.user.email
    # user = request.user
    email_id = request.user.id
    # 查询该用户对应的所有 OkxAccount 记录
    binance_accounts = BinanceAccount.objects.filter(email_id=email_id)
    # 将查询结果传递给模板
    context = {'binance_accounts': binance_accounts}
    # print(okx_accounts)
    # return render(request, 'account/test.html', context)
    return render(request, 'account/have_binance.html', context)


@login_required
def index_view(request):
    # print('我走的是index_view')
    if request.method == 'GET':
        # 获取当前用户
        email = request.user.email
        # user = request.user
        email_id = request.user.id
        # 查询该用户对应的所有 OkxAccount 记录
        okx_accounts = OkxAccount.objects.filter(email_id=email_id)
        binance_accounts = BinanceAccount.objects.filter(email_id=email_id)
        # 将查询结果传递给模板
        context = {'okx_accounts': okx_accounts,
                   'binance_accounts': binance_accounts}
        print(okx_accounts)
        # return render(request, 'account/test.html', context)
        return render(request, 'account/index.html', locals())
    if request.method == 'POST':
        okx_api_key = request.POST.get('okxApiKey')
        print(okx_api_key)
        binance_api_key = request.POST.get('binanceApiKey')
        print(binance_api_key)
        if okx_api_key and binance_api_key is None:
            add_okx_account_view(request)
        elif binance_api_key and okx_api_key is None:
            add_binance_account_view(request)

        return HttpResponseRedirect('/account/index/')


@login_required
def add_okx_account_view(request):
    global api_key
    email = request.user.email
    email_id = request.user.id
    # okx_account = OkxAccount.objects.filter(email=request.user)
    # api_key = request.okx_account.apikey
    # api_secret = request.okx_account.apisecret
    # api_password = request.okx_account.apipassword
    # email = request.user.email
    # if request.method == 'GET':
    #     print('我走的是get')
    # 获取该用户对应的OkxAccount对象
    try:
        okx_account = OkxAccount.objects.filter(email_id=email_id)
        # 获取该OkxAccount对象的apiKey, apiSecret, apiPassword
        # api_key = okx_account.apiKey
        # api_secret = okx_account.apiSecret
        # api_password = okx_account.apiPassword
        if okx_account:
            display_okx_accounts(request=request)
            # print('我都获取到了')
            # return HttpResponse(api_secret, api_password, api_key)
            # return HttpResponseRedirect('/account/have_okx/')
        # print('我走的是get')
        else:
            pass
            # GET返回页面
            # return render(request, "account/index.html", locals())
    except OkxAccount.DoesNotExist:
        # 如果该用户没有对应的OkxAccount对象，则返回空
        api_key = None
        api_secret = None
        api_password = None
        # print(api_key, api_secret, api_password)
        # if api_key and api_secret and api_password:
    if request.method == 'POST':
        api_key = request.POST.get('okxApiKey')
        api_secret = request.POST.get('okxApiSecret')
        api_password = request.POST.get('okxApiPassword')
        email = request.user
        account = OkxAccount(apiKey=api_key, apiSecret=api_secret, apiPassword=api_password, email=email)
        account.save()
        print(api_key, api_secret, api_password)
        # display_okx_accounts(request=request)
        display_okx_accounts(request=request)
        return render(request, 'account/have_okx.html', locals())
        # return HttpResponse('success')
        # return HttpResponseRedirect('/accounts/list/')  # 重定向到账户列表页面
    else:
        okx_account = OkxAccount.objects.filter(email_id=email_id)
        print(okx_account)
        if not okx_account:
            return render(request, 'account/index.html', locals())
        # return HttpResponse('fail')
        else:
            display_okx_accounts(request=request)
            return render(request, 'account/have_okx.html', locals())
        # return render(request, 'account/index.html',locals())
        # return HttpResponseRedirect('http://localhost:8000/account/have_okx')  # 重定向到添加账户页面
        # return render(request, 'add_account.html')

    # return render(request, 'account/index.html',locals())


@login_required
def add_binance_account_view(request):
    global api_key
    email = request.user.email
    email_id = request.user.id
    # 获取该用户对应的BinanceAccount对象
    try:
        binance_account = BinanceAccount.objects.filter(email_id=email_id)
        # 获取该OkxAccount对象的apiKey, apiSecret, apiPassword
        # api_key = okx_account.apiKey
        # api_secret = okx_account.apiSecret
        # api_password = okx_account.apiPassword
        if binance_account:

            display_binance_accounts(request=request)
            # print('我都获取到了')
            # return HttpResponse(api_secret, api_password, api_key)
            # return HttpResponseRedirect('/account/have_okx/')
        # print('我走的是get')
        else:
            pass
            # GET返回页面
            # return render(request, "account/index.html", locals())
    except BinanceAccount.DoesNotExist:
        # 如果该用户没有对应的OkxAccount对象，则返回空
        api_key = None
        api_secret = None
        api_password = None
        # print(api_key, api_secret, api_password)
        # if api_key and api_secret and api_password:
    if request.method == 'POST':
        api_key = request.POST.get('binanceApiKey')
        # api_secret = request.POST.get('binanceApiSecret')
        api_password = request.POST.get('binanceApiPassword')
        email = request.user
        account = BinanceAccount(apiKey=api_key, apiPassword=api_password, email=email)
        account.save()
        print(api_key, api_password)
        # display_okx_accounts(request=request)
        display_binance_accounts(request=request)
        return render(request, 'account/have_binance.html', locals())
        # return HttpResponse('success')
        # return HttpResponseRedirect('/accounts/list/')  # 重定向到账户列表页面
    else:
        display_binance_accounts(request=request)
        return render(request, 'account/have_binance.html', locals())
        # return render(request, 'account/index.html',locals())
        # return HttpResponseRedirect('http://localhost:8000/account/have_okx')  # 重定向到添加账户页面
        # return render(request, 'add_account.html')

    # return render(request, 'account/index.html',locals())


def have_okx_account(request):
    email = request.user.email
    # api_key = request.OkxAccount.api_key
    # api_secret = request.OkxAccount.api_secret
    # api_password = request.OkxAccount.api_password
    # if api_key and api_secret and api_password:
    #     return HttpResponse(api_secret, api_password, api_key)
    #     # return render(request, 'account/have_okx.html', locals())
    # else:
    return render(request, 'account/have_okx.html', locals())


def have_binance_account(request):
    email = request.user.email
    return render(request, 'account/have_binance.html', locals())
