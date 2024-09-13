from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def signin(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('pass1')

        chech_user = authenticate(username=email,password=passw)
        if chech_user and chech_user.is_active:
            login(request,chech_user)
            request.session['username']=chech_user.first_name
            context.update({'message':'Login successfull !!','class':'alert-success'})
            return HttpResponseRedirect(reverse('index'))
        else:
            context.update({'message':'Invalid Credentials !!','class':'alert-danger'})

    return render(request,'login.html',context)


def index(request):
    d={}
    if request.session.get('username'):
        FN = request.session.get('username')
        user = User.objects.get(first_name=FN)
        d['user'] = user 
    d["All"] = User.objects.all()  
    return render(request,'index.html',d)

def about(request):
    return render(request,'about.html')

def blog(request):
    return render(request,'blog.html')

def contact_us(request):
    d={}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        sub = request.POST.get('subject')
        msg = request.POST.get('message')

        obj = Contact(name=name,email=email,subject=sub,message=msg)
        obj.save()
        d['message']=f'Dear {name} ,Thanks for your time !!'
        
    return render(request,'contact.html',d)

def register(request):
    d={}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('mobile')
        password = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        if password == password2:
            try:
                usr = User.objects.create_user(username=email,email=email,password=password)
                usr.first_name = name
                usr.save()
                
                profile = Profile(user=usr,contact=number)
                profile.save()
                d['status1'] = f"Dear {name}, Register Successfully !!"
            except :
                d['status2'] = f"Dear {name},This email already exists !!"
            return redirect('/login')
        else:
            messages.warning(request,'Passwords do not match!!')
            return redirect('/register')


    return render(request,'register.html',d)


def booking(request):
    return render(request,'booking.html')

@login_required(login_url='login')
def orderhistory(request):
    OH = Order_history.objects.filter(user=request.user)
    return render(request,'orderhistory.html',{'OH':OH})

def menu(request):
    if request.method == "POST":
        pass
    else:
        Cat = Category.objects.all()
    return render(request,'menu.html',{'category':Cat})

def single(request):
    return render(request,'single.html')

def team(request):
    return render(request,'team.html')

def dish(request,id):
    c=Category.objects.get(pk=id)
    d=Dish.objects.filter(category=c)
    return render(request,'dish.html',{'dish':d})

@login_required(login_url='login')
def cart(request,id):
    user = User.objects.get(username=request.user)
    obj = Dish.objects.get(id=id)
    NWO,created = Dish_cart.objects.get_or_create(user=user,name=obj)
    
    if created:
        NWO.ammount=obj.price
        NWO.counter = 1
    else:
        NWO.counter += 1
        NWO.ammount=obj.price*NWO.counter
    NWO.save()
    
    cart_list = Dish_cart.objects.filter(user=user)
    m = 0
    for d in cart_list:
        m = m + (d.name.price * d.counter)

    return render(request,'cart.html',{'cart':cart_list,'M':m})

@login_required(login_url='login')
def cartall(request):
    user = User.objects.get(username=request.user)
    cart_list = Dish_cart.objects.filter(user =user )
    m = 0
    for d in cart_list:
        m = m + (d.name.price * d.counter)

    return render(request,'cart.html',{'cart':cart_list,'M':m})

def qntysub(request,id):
    obj = Dish.objects.get(id=id)
    meal = Dish_cart.objects.get(user=request.user,name=obj)
    if meal.counter > 0:
        meal.counter -= 1
        meal.ammount -= obj.price
        meal.save()
    Dish_cart.objects.filter(counter=0).delete()
    
    return redirect('/cart')

def qntyadd(request,id):
    obj = Dish.objects.get(id=id)
    meal = Dish_cart.objects.get(user=request.user,name=obj)
    meal.counter += 1
    meal.ammount += obj.price
    meal.save()
    
    return redirect('/cart')

def removedish(request,id):
    obj = Dish.objects.get(id=id)
    Dish_cart.objects.get(user=request.user,name=obj).delete()
    return redirect('/cart')

@login_required(login_url='login')
def order(request):
    user = User.objects.get(username=request.user)
    cart_list = Dish_cart.objects.filter(user =user)
    m = 0
    disc = 0
    for d in cart_list:
        m = m + (d.name.price * d.counter)
        disc = disc + (d.counter * d.name.discount_price)
        
    Shipping_charge = 50.0
    ta = m + Shipping_charge-disc
    return render(request,'order.html',{'order':cart_list,'am':m,'sc':Shipping_charge,'ta':ta,'disc':disc,"User":user})

@login_required(login_url='login')
def payment(request):
    user = User.objects.get(username=request.user)
    cartdish = Dish_cart.objects.filter(user=user)
    for food in cartdish:
        Order_history(user=user,product=food.name,quantity=food.counter,ammount=food.counter*food.name.price).save()
        food.delete()

    return redirect('orderhistory')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))