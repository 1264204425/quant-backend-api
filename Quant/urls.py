"""Quant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from account import views

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'), #quant
    # path('', views.add_okx_account_view, name='index'),
    # path('add_okx/', views.add_okx_account_view, name='index'),
    # path('', views.have_okx_account, name='index'),
    path('index/', views.index_view, name='index'),
    path('index/user/login/', user_views.login_view, name='login'),
    path('chart/', include('chart.urls')),
    # path('index/ahr999', views.ahr999_view), #quant
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),
    path('account/', include('account.urls')),

    # path('login/', views.login_view),
    # path('register/', views.register_view),
    # # path('forgot/', views.forgot_view),
    # path('index/', views.index_view),
]
