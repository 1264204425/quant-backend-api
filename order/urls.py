from django import views
from django.urls import path
from . import views

urlpatterns = [
    # path('okx_order_list/?okx_refresh_orders', views.okx_refresh_orders_view, name='okx_refresh_orders'),
    path("okx_order_list/", views.okx_order_list_view, name="order"),
    # path('binance_order_list/', views.binance_order_list_view, name='binance_order_list'),
    path('binance_order_list/', views.okx_order_list_view, name='binance_order_list'),
    path('test/', views.display_okx_positions, name='test'),
    path('get_history_orders/', views.okx_history_excel, name='get_history_orders'),
    path('okx_refresh_orders/', views.okx_refresh_orders_view, name='okx_refresh_orders'),

]