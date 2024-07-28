from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from shop.form import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shoptemp/shopindex.html",{"products":products})

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shoptemp/cart.html",{"cart":cart})
    else:
        return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect("/login")
    return render(request,"shoptemp/login.html")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")

def reg(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now...!")
            return redirect('/login')
    return render(request,"shoptemp/reg.html",{'form':form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shoptemp/collections.html",{"catagory":catagory})

def collectionsview(request,name):
    if (Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(Catagory__name=name)
        return render(request,"shoptemp/products/index.html",{"products":products,"Catagory_name":name})
    else:
        messages.warning(request,"No such Category found")
        return redirect('collections')

def product_details(request,cname,pname):
    if (Catagory.objects.filter(name=cname,status=0)):
        if (Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shoptemp/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No such Product found")
            return redirect('collections')
    else:
        messages.error(request,"No such Category found")
        return redirect('collections')


def add_to_cart(request):
    if request.headers.get('X-requested-with')=='XMLHTTpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)


def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shoptemp",{"cart":cart_page})
    else:
        return redirect("/")
