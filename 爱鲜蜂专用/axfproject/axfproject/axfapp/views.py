from django.shortcuts import render, redirect
from .models import wheel, nav, mustbuy,shop,MainShow,FoodType,Goods,User,Cart
# Create your views here.
import time
import random
from django.conf import settings
import os

def main(request):

    return render(request, 'axfproject/base.html')

def home(request):
    wheelsList = wheel.objects.all()
    navList = nav.objects.all()
    mustbuyList = mustbuy.objects.all()
    shopList = shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]

    mainList = MainShow.objects.all()

    return render(request, 'axfproject/home.html',
    {"title":"主页","wheelsList":wheelsList, "navList": navList,
    "mustbuyList":mustbuyList, "shop1":shop1, "shop2":shop2,
     "shop3":shop3,"shop4":shop4, "mainList":mainList})

def market(request, categoryid, cid, sortid):
    leftSlider = FoodType.objects.all()

    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid=cid)

    #排序

    if sortid == '1':
        productList = productList.order_by("productnum")
    elif sortid == '2':
        productList = productList.order_by("price")
    elif sortid == '3':
        productList = productList.order_by("-price")


    group = leftSlider.get(typeid=categoryid)
    childList = []
    childnames = group.childtypenames
    arr1 = childnames.split("#")
    for str in arr1:
        arr2 = str.split(":")
        obj = {"childName":arr2[0], "childId":arr2[1]}
        childList.append(obj)

    return render(request, 'axfproject/market.html',
                  {"title":"闪购","leftSlider":leftSlider, "productList":productList, "childList":childList
                   , "categoryid":categoryid, "cid":cid})

def cart(request):
    return render(request, 'axfproject/cart.html',{"title":"购物车"})
#修改购物车
def changecart(request, flag):
    #判断是否登录
    token = request.session.get('token')
    if token == 'None':
        #么有登录
        return JsonResponse({'data':-1, 'status':'error'})

    productid = request.POST.get('productid')
    product = Goods.objects.get(productid=productid)
    user = User.objects.get(userToken=token)

    if flag == '0':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        if carts.count() == 0:
            #增加一条订单
            c= Cart.createcart(user.userAccount,productid,1,product.price,True,product.productimg,product.productlongname,False)
            c.save()
            pass
        else:
            try:
                onecart = carts.get(productid=productid)
            except  Cart.DoesNotExist as e:
                pass
    elif flag == '1':
        pass
    elif flag == '2':
        pass
    elif flag == '3':
        pass


def mine(request):
    username = request.session.get('username', "未登录")
    return render(request, 'axfproject/mine.html',{"title":"我的", "username":username})

from .forms.login import LoginForm
from django.http import HttpResponse
def login(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            try:
                user = User.objects.get(userAccount = nameid)
                if user.userpasswd != pswd:
                    return redirect('/login/')


            except User.DoesNotExist as e:
                return redirect('/login/')


            token = time.time() + random.randrange(1, 10000000000)
            user.userToken = str(token)
            user.save()
            request.session['username'] = user.userName
            request.session['token'] = user.userToken
            return redirect('/mine/')

        else:
            return render(request, 'axfproject/login.html', {'title':'登录','form':f,'error':f.errors})
    else:
        f = LoginForm()
        return render(request, 'axfproject/login.html', {"title":"登录","form":f})



def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get('userAccount')
        userPasswd = request.POST.get('userPass')
        userName = request.POST.get('userName')
        userPhone = request.POST.get('userPhone')
        userAdderss = request.POST.get('userAdderss')
        userRank = 0
        token = time.time() + random.randrange(1 , 10000000000)
        userToken = str(token)

        f = request.FILES['userImg']
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + '.png')
        with open(userImg, 'wb') as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()
        request.session['username'] = userName
        request.session['token'] = userToken
        return redirect('/mine/')


    else:
        return render(request, 'axfproject/register.html', {'title':'注册'})


from django.http import JsonResponse
def checkuserid(request):
    userid = request.POST.get('userid')

    try:
        user = User.objects.get(userAccount = userid)
        return JsonResponse({'data':'该用户已被注册','status':"error"})
    except User.DoesNotExist as e:
        return JsonResponse({'data':'ok','status':"success"})

from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')