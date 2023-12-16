from django.db import models
from django.contrib.auth.models import User
from django.db.models import ExpressionWrapper,FloatField
from django.db.models import F
from django.db.models.functions import Abs


# Create your models here.

class OkxNowPositions(models.Model):
    instId = models.CharField(max_length=50)  # 交易对
    posSide = models.CharField(max_length=50)  # 持仓方向
    pos = models.IntegerField()  # 持仓量
    lever = models.IntegerField()  # 杠杆倍数
    avgPx = models.FloatField()  # 持仓均价
    markPx = models.FloatField()  # 标记价格
    liqPx = models.FloatField(null=True, blank=True)  # 预估强平价格
    mgnRatio = models.FloatField()  # 维持保证金率
    cTime_change = models.DateTimeField(null=True)
    cTime = models.CharField(max_length=50)  # 仓位创建的时间戳
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.IntegerField(default='1')
    # 定义计算字段 benefits
    benefits = ExpressionWrapper((F('markPx') - F('avgPx')) / F('avgPx') * F('lever') * 100 * F('pos') / Abs(F('pos')),
                                 output_field=FloatField())


    def __str__(self):
        return f"{self.instId} - {self.posSide}"


# __str__() 是 Python 中的一个特殊方法，用于指定当对象被打印为字符串时应该返回的内容 如果某个持仓对象的 instId 属性为 BTC-USDT-SWAP，
# posSide 属性为 long，则 print() 该对象时将返回 BTC-USDT-SWAP - long。

class OkxHistoryPositions(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户
    cTime_change = models.DateTimeField()
    cTime = models.CharField(max_length=50)  # 仓位创建的时间戳
    ccy = models.CharField(max_length=10)  # 币种
    closeAvgPx = models.FloatField()  # 平均平仓价格
    closeTotalPos = models.IntegerField()  # 平仓总量
    direction = models.CharField(max_length=10)  # 仓位方向
    instId = models.CharField(max_length=50)  # 交易对
    instType = models.CharField(max_length=10)  # 交易类型
    lever = models.FloatField()  # 杠杆倍数
    mgnMode = models.CharField(max_length=10)  # 保证金模式
    openAvgPx = models.FloatField()  # 平均开仓价格
    openMaxPos = models.IntegerField()  # 最大开仓量
    pnl = models.FloatField()  # 持仓盈亏
    pnlRatio = models.FloatField()  # 持仓盈亏率
    posId = models.CharField(max_length=50)  # 持仓ID
    # triggerPx = models.FloatField(null=True)  # 触发价格
    type = models.IntegerField()  # 仓位类型
    uTime_change = models.DateTimeField(null=True)
    uTime = models.CharField(max_length=50) # 仓位更新的时间戳
    uly = models.CharField(max_length=50)  # 标的指数
