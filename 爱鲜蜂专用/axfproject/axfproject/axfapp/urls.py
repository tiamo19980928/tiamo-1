from django.urls import path
from . import views
urlpatterns=[
    path('', views.main,name='main'),
    path('home/',views.home,name='home'),
    path('market/<categoryid>/<cid>/<sortid>/',views.market,name='market'),
    path('cart/',views.cart,name='cart'),
    path('mine/',views.mine,name='mine'),

    #登录
    path('login/',views.login,name='login'),

    path('register/',views.register,name='register'),

    path('checkuserid/',views.checkuserid,name='checkuserid'),

    path('quit/',views.quit,name='quit'),

    path('changecart/<productid>/', views.changecart, name='changecart'),
]
