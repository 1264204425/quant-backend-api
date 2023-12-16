import os
import time

import openpyxl
import pandas as pd
import pytz
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, FloatField
from django.db.models.functions import Abs
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render
import ccxt
import datetime

from django.contrib.auth.models import User
from order.models import OkxHistoryPositions, OkxNowPositions
import json
from django.db.models import F
from django.db.models import Value, IntegerField

from user.models import OkxAccount


# Create your views here.
#
@login_required(login_url='/index/user/login/')
# ，在视图函数中查询该用户当前持仓，然后将结果传递给模板，使用模板语言进行渲染.
def display_okx_positions(request):
    # 获取当前用户
    email = request.user.email
    # user = request.user
    email_id = request.user.id
    # 计算收益率
    benefits = ExpressionWrapper((F('markPx') - F('avgPx')) / F('avgPx') * F('lever') * 100 * F('pos') / Abs(F('pos')),
                                 output_field=FloatField())
    # benefits_counts = ExpressionWrapper(benefits * F('markPx'), output_field=FloatField())
    pnlRatio100 = ExpressionWrapper(F('pnlRatio') * Value(100), output_field=FloatField())
    # 查询该用户对应的所有 OkxAccount 记录
    active_okx_now_positions = OkxNowPositions.objects.filter(email_id=email_id, active=1).annotate(benefits=benefits)
    print(active_okx_now_positions)
    now_positions = OkxNowPositions.objects.filter(email_id=email_id).annotate(benefits=benefits)
    history_positions = OkxHistoryPositions.objects.filter(email_id=email_id).order_by('id').annotate(pnlRatio100=pnlRatio100)
    print('开始分页')
    # 创建 Paginator 对象，每页显示 10 条数据
    paginator = Paginator(history_positions, 10)
    # 获取当前页码（默认为第一页）
    page_number = request.GET.get('page')
    # 获取当前页面的 Article 对象列表
    page_obj = paginator.get_page(page_number)

    context = {'now_positions': active_okx_now_positions,
               'history_positions': history_positions}
    # print(okx_accounts)
    # return render(request, 'account/test.html', context)
    return render(request, 'order/okx_order.html', locals())
    # return render(request, 'order/test.html', locals())


def display_binance_positions(request):
    # 获取当前用户
    email = request.user.email
    # user = request.user
    email_id = request.user.id
    # 计算收益率
    benefits = ExpressionWrapper((F('markPx') - F('avgPx')) / F('avgPx') * F('lever') * 100 * F('pos') / Abs(F('pos')),
                                 output_field=FloatField())
    # benefits_counts = ExpressionWrapper(benefits * F('markPx'), output_field=FloatField())
    # 查询该用户对应的所有 OkxAccount 记录
    now_positions = OkxNowPositions.objects.filter(email_id=email_id).annotate(benefits=benefits)
    history_positions = OkxHistoryPositions.objects.filter(email_id=email_id)
    # 创建 Paginator 对象，每页显示 10 条数据
    paginator = Paginator(history_positions, 10)
    # 获取当前页码（默认为第一页）
    page_number = request.GET.get('page')
    # 获取当前页面的 Article 对象列表
    page_obj = paginator.get_page(page_number)

    context = {'now_positions': now_positions,
               'history_positions': history_positions}
    # print(okx_accounts)
    # return render(request, 'account/test.html', context)
    return render(request, 'order/binance_order.html', locals())
    # return render(request, 'order/test.html', locals())


# excel
def okx_history_excel(request):
    email_id = request.user.id
    history_positions = OkxHistoryPositions.objects.filter(email_id=email_id)

    # 将 QuerySet 对象转换为 Pandas 数据类型
    df = pd.DataFrame(list(
        history_positions.values('id', 'instId', 'openMaxPos', 'closeAvgPx', 'openAvgPx', 'lever', 'cTime', 'uTime')))

    df['cTime'] = df['cTime'].astype(float).apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(x / 1000)))
    df['uTime'] = df['uTime'].astype(float).apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(x / 1000)))
    # print(df)

    # 导出数据到 Excel 文件
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    output_dir = os.path.join(
        parent_dir + '\\Quant\\order\\static\\assets\\okx_history_positions\\' + str(email_id) + 'orders.xlsx')
    # print(output_dir)
    df.to_excel(output_dir, index=False)
    # print('我写入了')
    filename = os.path.basename(output_dir)
    # print(filename)
    # 返回生成的 Excel 文件给用户下载
    # with open(output_dir, 'rb') as f:
    #     response = FileResponse(f, as_attachment=True)
    #     response['Content-Type'] = 'application/vnd.ms-excel' # 设置响应头 表示发送的内容是 Excel 文件
    #     response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename) # 设置响应头 表示以附件形式发送文件
    #     return response
    #     # 返回生成的 Excel 文件给用户下载
    with open(output_dir, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


def get_okx_order_list():
    return None


def binance_order_list_view(request):
    return render(request, 'order/binance_order.html')


def okx_refresh_orders_view(request):
    print('我走okx_order_list_view')
    email = request.user
    email_id = request.user.id
    okx_accounts = OkxAccount.objects.filter(email_id=email_id)
    now_orders = OkxNowPositions.objects.filter(email_id=email_id)
    history_orders = OkxHistoryPositions.objects.filter(email_id=email_id)
    # print('我走的api')
    now_orders = []
    history_orders = []
    for okx_account in okx_accounts:
        print('我走到for了')
        apiKey = okx_account.apiKey
        apiSecret = okx_account.apiSecret
        apiPassword = okx_account.apiPassword
        OKEX_CONFIG = {
            'apiKey': apiKey,
            'secret': apiSecret,
            'password': apiPassword,
            'proxies': {
                'http': 'http://localhost:57370',
                'https': 'http://localhost:57370',
            },
        }
        print(OKEX_CONFIG)
        exchange = ccxt.okex(OKEX_CONFIG)
        try:
            now_order = exchange.privateGetAccountPositions()
            history_order = exchange.privateGetAccountPositionsHistory()
            # 整理持仓数据
            save_now_positions_to_db(extract_now_positions(now_order), user_email=email)
            save_history_positions_to_database(extract_history_positions(history_order), user_email=email)
        except Exception as e:
            print(e)
            return HttpResponse('出错了请检查api或稍后再试')
        # history_orders.append(history_order)
        # now_orders.append(now_order)
    print('准备展示')
    display_okx_positions(request)

    return HttpResponseRedirect('/order/okx_order_list')


def okx_order_list_view(request):
    print('我走okx_order_list_view')
    email = request.user
    email_id = request.user.id
    okx_accounts = OkxAccount.objects.filter(email_id=email_id)
    now_orders = OkxNowPositions.objects.filter(email_id=email_id)
    history_orders = OkxHistoryPositions.objects.filter(email_id=email_id)
    if now_orders and history_orders:
        return display_okx_positions(request)
    else:
        # print('我走的api')
        now_orders = []
        history_orders = []
        for okx_account in okx_accounts:
            print('我走到for了')
            apiKey = okx_account.apiKey
            apiSecret = okx_account.apiSecret
            apiPassword = okx_account.apiPassword
            OKEX_CONFIG = {
                'apiKey': apiKey,
                'secret': apiSecret,
                'password': apiPassword,
                'proxies': {
                    'http': 'http://localhost:57370',
                    'https': 'http://localhost:57370',
                },
            }
            print(OKEX_CONFIG)
            exchange = ccxt.okex(OKEX_CONFIG)
            try:
                now_order = exchange.privateGetAccountPositions()
                history_order = exchange.privateGetAccountPositionsHistory()
                # 整理持仓数据
                save_now_positions_to_db(extract_now_positions(now_order), user_email=email)
                save_history_positions_to_database(extract_history_positions(history_order), user_email=email)
            except Exception as e:
                print(e)
                return HttpResponse('出错了请检查api或稍后再试')
            # history_orders.append(history_order)
            # now_orders.append(now_order)
        return display_okx_positions(request)
        # return render(request, 'order/okx_order.html', locals())


# 获取用户api key
def get_okx_api_key(request):
    email = request.user.email
    print(email)
    okx_accounts = OkxAccount.objects.filter(email=email)
    for okx_account in okx_accounts:
        apiKey = okx_account.apiKey
        apiSecret = okx_account.apiSecret
        apiPassword = okx_account.apiPassword
        OKEX_CONFIG = {
            'apiKey': apiKey,
            'secret': apiSecret,
            'password': apiPassword,
            'proxies': {
                'http': 'http://localhost:57370',
                'https': 'http://localhost:57370',
            },
        }
        return OKEX_CONFIG


# 获取用户历史持仓
def get_okx_history_positions(OKEX_CONFIG, exchange):
    history_order = exchange.privateGetAccountPositionsHistory()

    return history_order


# 获取用户当前持仓
def get_okx_now_positions(OKEX_CONFIG, exchange):
    now_order = exchange.privateGetAccountPositions()
    return now_order


# 整理历史持仓数据
def extract_history_positions(json_data):
    json_data = json.dumps(json_data)
    positions_data = []
    data = json.loads(json_data)
    if 'data' in data:
        for item in data['data']:
            position = {}
            # position['cTime'] = item['cTime']
            position['cTime_change'] = datetime.datetime.fromtimestamp(int(item['cTime']) / 1000.0).strftime(
                '%Y-%m-%d %H:%M:%S.%f')  # 仓位创建的时间戳
            position['cTime'] = int(item['cTime'])  # 仓位创建的时间戳
            position['ccy'] = item['ccy']  # 币种
            position['closeAvgPx'] = item['closeAvgPx']  # 平仓均价
            position['closeTotalPos'] = item['closeTotalPos']  # 平仓总持仓
            position['direction'] = item['direction']  # 开仓方向
            position['instId'] = item['instId']  # 交易对
            position['instType'] = item['instType']  # 合约类型
            position['lever'] = item['lever']  # 杠杆倍数
            position['mgnMode'] = item['mgnMode']  # 保证金模式
            position['openAvgPx'] = item['openAvgPx']  # 开仓均价
            position['openMaxPos'] = item['openMaxPos']  # 开仓最大持仓
            position['pnl'] = item['pnl']  # 持仓盈亏
            position['pnlRatio'] = item['pnlRatio']  # 持仓盈亏率
            position['posId'] = item['posId']  # 仓位ID
            # print(position['posId'])
            position['triggerPx'] = item.get('stopPx', '')  # 止盈止损价格 get()方法获取字典中对应键的值，如该值不存在则返回一个默认值（本例中为一个空字符串）
            position['type'] = 1 if item[
                                        'mgnMode'] == 'cross' else 2  # 1:全仓 2:逐仓 Cross:Cross Margin,又称全仓模式 Isolate:Isolated Margin,又称逐仓模式
            position['uTime_change'] = datetime.datetime.fromtimestamp(int(item['uTime']) / 1000.0).strftime(
                '%Y-%m-%d %H:%M:%S.%f')  # 仓位最后一次更新的时间戳
            position['uTime'] = int(item['uTime'])  # 仓位最后一次更新的时间戳
            position['uly'] = item['uly']  # 交易对
            positions_data.append(position)
    return positions_data


# 整理当前持仓数据
def extract_now_positions(data):
    positions = []
    for item in data['data']:
        position = {}
        position['instId'] = item['instId']  # 交易对
        position['posSide'] = item['posSide']  # 持仓方向
        position['pos'] = int(item['pos'])  # 持仓量
        position['lever'] = item['lever']  # 杠杆倍数
        position['avgPx'] = float(item['avgPx'])  # 持仓均价
        position['markPx'] = float(item['markPx'])  # 标记价格
        position['liqPx'] = None if item['liqPx'] == '' else float(item['liqPx'])  # 预估强平价格
        position['mgnRatio'] = float(item['mgnRatio'])  # 维持保证金率
        position['cTime_change'] = datetime.datetime.fromtimestamp(int(item['cTime']) / 1000.0).strftime(
            '%Y-%m-%d %H:%M:%S.%f')  # 仓位创建的时间戳
        position['cTime'] = item['cTime']
        positions.append(position)
    return positions


# 保存历史持仓数据到数据库
def save_history_positions_to_database(data, user_email):
    print('save_history_positions_to_database')
    positions = data
    print(positions)
    for position in positions:
        history_position = OkxHistoryPositions()
        history_position.email = user_email
        history_position.cTime_change = position['cTime_change']  # 仓位创建的时间戳
        history_position.cTime = position['cTime']  # 仓位创建的时间戳
        history_position.instId = position['instId']  # 交易对
        history_position.ccy = position['ccy']  # 币种
        history_position.direction = position['direction']  # 开仓方向
        history_position.posId = position['posId']  # 仓位ID
        history_position.instType = position['instType']  # 合约类型
        history_position.lever = position['lever']  # 杠杆倍数
        history_position.mgnMode = position['mgnMode']  # 保证金模式
        history_position.pnlRatio = position['pnlRatio']  # 持仓盈亏率
        history_position.pnl = position['pnl']  # 持仓盈亏
        history_position.openMaxPos = position['openMaxPos']  # 开仓最大持仓
        history_position.openAvgPx = position['openAvgPx']  # 开仓均价
        history_position.closeTotalPos = position['closeTotalPos']  # 平仓总持仓
        history_position.closeAvgPx = position['closeAvgPx']  # 平仓均价
        history_position.uTime_change = position['uTime_change']  # 仓位最后一次更新的时间戳
        history_position.uTime = position['uTime']  # 仓位最后一次更新的时间戳
        # history_position.triggerPx = position['triggerPx']  # 触发价格
        history_position.uly = position['uly']  # 交易对
        history_position.type = position['type']  # 1:全仓 2:逐仓
        existing_positions = OkxHistoryPositions.objects.filter(
            email_id=user_email,
            instId=history_position.instId,
            cTime=history_position.cTime,
        )
        # uTime=history_position.uTime
        # print(history_position.instId)
        # print(history_position.uTime)
        # print(history_position.email)
        # print(existing_positions)
        # print(connection.queries)
        # exit()
        if not existing_positions.exists():
            # print('保存你了')
            history_position.save()  # 保存到数据库


# 保存当前持仓数据到数据库
def save_now_positions_to_db(data, user_email):
    # positions_data = extract_now_positions(data)
    positions_data = data
    # print(positions_data)
    # positions = data
    OkxNowPositions.objects.filter(email_id=user_email).update(active=0)
    for positions in positions_data:
        position = OkxNowPositions()
        position.email = user_email
        position.instId = positions['instId']
        position.posSide = positions['posSide']
        position.pos = positions['pos']
        position.lever = positions['lever']
        position.avgPx = positions['avgPx']
        position.markPx = positions['markPx']
        position.liqPx = positions['liqPx']
        position.mgnRatio = positions['mgnRatio']
        position.cTime_change = positions['cTime_change']
        # position.cTime_change = datetime.datetime.strptime(positions['cTime'], '%Y-%m-%d %H:%M:%S.%f')
        position.cTime = positions['cTime']
        # position.benefits =
        existing_positions = OkxNowPositions.objects.filter(
            email_id=user_email,
            instId=position.instId,
            cTime=position.cTime,
            active = 1,
        )
        print(position.email)
        # print(position.instId)
        # print( position.cTime)
        print(existing_positions)
        # exit()
        if not existing_positions.exists():
            position.save()
