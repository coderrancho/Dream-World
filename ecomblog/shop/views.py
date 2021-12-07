from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,orderUpdate,Signup
from math import ceil
from django.core.serializers import serialize
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum
import tkinter as tk 
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# Create your views here.
MERCHANT_KEY = 'LOPeRIFkOA3DGwCp'
def index(request):
    books=Product.objects.filter(subcategory='book')
    bags = Product.objects.filter(subcategory='bag')
    boxes = Product.objects.filter(subcategory='box')
    pens = Product.objects.filter(subcategory='pen')
    toys = Product.objects.filter(subcategory='toy')
    countProd=[books,bags,boxes,pens,toys]
    countList=[18,12,12,12,12]
    allProds=[]
    for j in range(5):
        i=countList[j]
        nSlides3 = i// 3 + ceil(i / 3 - i // 3)
        nSlides2 = i// 2 + ceil(i / 2 - i // 2)
        nSlides1=i
        if width<=792:
            nSlides=nSlides1
            divider=1
        elif width<=1000:
            nSlides=nSlides2
            divider=2
        else:
            nSlides=nSlides3
            divider=3
        allProds.append([countProd[j],nSlides,range(1,nSlides),divider])

    params={'allProds':allProds}
    return render(request,'shop/index.html',params)

def searchMatch(query, item):
    if query in item.product_name.lower() or query in item.category.lower() or query in item.desc.lower() or query in item.subcategory.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    books = Product.objects.filter(subcategory='book')
    bags = Product.objects.filter(subcategory='bag')
    boxes = Product.objects.filter(subcategory='box')
    pens = Product.objects.filter(subcategory='pen')
    toys = Product.objects.filter(subcategory='toy')
    countProd = [books, bags, boxes, pens, toys]
    allProds = []
    for j in range(5):
        prod=[item for item in countProd[j] if searchMatch(query,item)]
        i = len(prod)
        # nSlides2 = i // 2 + ceil(i / 2 - i // 2)
        # nSlides = i // 3 + ceil(i / 3 - i // 3)
        nSlides=i
        if(len(prod)!=0):
            allProds.append([prod, nSlides, range(1, nSlides)])

    params = {'allProds': allProds, "msg": "",'query':query}
    if len(allProds) == 0 or len(query) < 3:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)
def about(request):
    return render(request,'shop/about.html')


def contact(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        if(len(name)<2 and len(email)<6 and len(phone)<10 and len(desc)<5):
            messages.error(request,  'Enter relevant data')
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request, 'Thanks for putting up your query')

        return render(request, 'shop/contact.html')

    return render(request, 'shop/contact.html')


def tracker(request):
    if(request.method=='POST'):
        order_id=request.POST.get('order_id','')
        email=request.POST.get('email','')
        try:
            order=Order.objects.filter(order_id=order_id,email=email)
            if(len(order)>0):
                update=orderUpdate.objects.filter(order_id=order_id)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps(updates,default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")

        except Exception as e:
            return HttpResponse("{}")
    return render(request, 'shop/tracker.html')



def productview(request,myid):
    product=Product.objects.filter(id=myid)
    return render(request, 'shop/productview.html',{'product':product[0]})


def checkout(request):
    if request.method=='POST':
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address1=request.POST.get('address1','')
        address2=request.POST.get('address2','')
        city=request.POST.get('city','')
        phone=request.POST.get('phone','')
        zip_code=request.POST.get('zip_code','')
        password=request.POST.get('password','')
        checkPassword = Signup.objects.filter(email=email,password=password)
        thank=False
        if(len(checkPassword)>=1):
            order=Order(items_json= items_json,name=name,email=email,address1=address1,address2=address2,city=city,phone=phone,zip_code=zip_code, amount=amount)
            order.save()
            id = order.order_id
            update = orderUpdate(order_id=id, update_desc="Your order have been placed successfully")
            update.save()
            # Request paytm to transfer the amount to your account after payment by user
            param_dict = {

                'MID': 'YxbKJj73792936211082',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            thank=True

        else:
            messages.error(request, "Sorry, order can't be placed. Make sure to enter correct email and password")
        return render(request, 'shop/paytm.html', {'param_dict': param_dict,'thank':thank})

    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def cart(request):
    return render(request, 'shop/cart.html')



def signup(request):
    if(request.method=='POST'):
        firstname= request.POST.get('firstname', '')
        lastname= request.POST.get('lastname', '')
        email= request.POST.get('email', '')
        city= request.POST.get('city', '')
        zipcode= request.POST.get('zipcode', '')
        password= request.POST.get('password', '')
        checkPassword=Signup.objects.filter(password=password)
        if(len(checkPassword)>=1):
            messages.error(request, 'Password already exists. Enter unique password')
        elif(len(password)<6):
            messages.error(request, 'Password too short. Enter at least 6 characters')
        else:
            signup=Signup(firstname=firstname,lastname=lastname,email=email,city=city,zipcode=zipcode,password=password)
            signup.save()
            return render(request, 'shop/login.html')
    return render(request, 'shop/signup.html')


def login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            account = Signup.objects.filter(email=email, password=password)
            if (len(account) > 0):
                return render(request,'shop/checkout.html')
            else:
                messages.error(request, 'This email and password does not exists')
        except Exception as e:
            return HttpResponse("Enter correct credentials")
    return render(request, 'shop/login.html')