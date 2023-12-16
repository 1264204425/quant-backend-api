from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view),
    # path('index/user/login/', views.login_view, name='login'),
    path('register/', views.register_view),
    # path('forgot/', views.forgot_view),
    path('index/', views.index_view),
    path('logout/', views.logout_view),
    # path('index/user/login/', views.login_view, name='login'),
    path('test_block/',views.test_block_view),
    path('block/', views.block_view),
    path('index/addokx/', views.addokxaccount_view),
    path('ahr999/', views.ahr999_view),
]