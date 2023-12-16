from django import views
from django.urls import path
from . import views

urlpatterns = [
    # path('test', views.test_view),
    path('index/', views.index_view, name='index'),
    path('add_okx_account/', views.add_okx_account_view, name=' add_okx_account'),
    path('add_binance_account/', views.add_binance_account_view, name='add_binance_account'),
    path('have_okx/', views.have_okx_account),  # 有okx账户
    path('have_binance/', views.have_binance_account),  # 有binance账户
    path('test/', views.display_okx_accounts),
    # path('okx_api/', views.okx_api, name='okx_api'),  # okx_api
    path('delete_okx_api/', views.delete_okx_account, name='delete_okx'),  # 删除okx api账户
    path('delete_binance_api/', views.delete_binance_account, name='delete_binance'),  # 删除binance api账户
]
