
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import CustomLoginForm
import json
import logging
from django.conf import settings
import requests
from .models import Category, Product
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
import uuid


from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    
    accessory = Product.objects.filter(category='accessory') [:6]
    men_products = Product.objects.filter(category='men')[:6]
    women_products = Product.objects.filter(category='women') [:6]
    kids_products = Product.objects.filter(category='kids')[:6]
    computer = Product.objects.filter(category='computer')[:6]
    appliances = Product.objects.filter(category='appliances')[:6]
    phones = Product.objects.filter(category='phones')[:6]
    # computer = Product.objects.filter(category='computer')[:6]
    
    recent_images = Product.objects.filter(image__isnull=False).order_by('-created_at')[:5]

    return render(request, 'home.html', {
       'accessory': accessory,
       'kids_products': kids_products,
        'men_products': men_products,
        'women_products': women_products,
        'recent_images': recent_images,
        'computer' : computer,
        'phones': phones,
        'appliances': appliances
    })
    
def search(request):
    query = request.GET.get('q', '')
    if query:
        results = Product.objects.filter(category__icontains=query)
        
      
        results_data = [{
            'id': product.id,        
            'name': product.name,
            'image': product.image,
            'price': product.price
            
        } for product in results]
    
    context = {
        'results_data' : results_data,
        'name' : 'Faith'
    }
    return render(request, 'search_result.html', context)


def category_list(request, slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_list.html', {'categories': categories, 'category': category, 'products': products})

def product_list(request, category=None):
    if category:
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True)
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'product_list.html', context)


def appliances(request):
    
    appliances = Product.objects.filter(category='appliances') [:6]
    return render(request, 'appliances.html', {
        'appliances': appliances
    } )


def fashion(request):
    return render(request, 'fashion.html',  )

def computer(request):
    computer = Product.objects.filter(category='computer') [:6]
    return render(request, 'computer.html', {
        'computer': computer
    } )

def games(request):
    games = Product.objects.filter(category='games') [:6]
    return render(request, 'games.html',  {
        'games': games
    })

def supermarket(request):
    supermarket = Product.objects.all() 
    return render(request, 'supermarket.html',  {
        'supermarket': supermarket
    })

def electronics(request):
    accessory = Product.objects.filter(category='accessory') [:6]
    return render(request, 'electronics.html',  {
        'accessory' : accessory
    })


def explore(request):
    
    return render(request, 'explore.html',  )

def office(request):
    return render(request, 'office.html',  )

def health(request):
    health = Product.objects.filter(category='health') [:6]
    return render(request, 'health.html', {
        'health' : health
    } )


def phones(request):
    phones = Product.objects.filter(category='phones') [:6]
    return render(request, 'phones.html', {
        'phones' : phones
    } )


def accessory(request,):
    
    products = Product.objects.filter(category='accessory')
    
    return render(request, 'accessory.html', {
        'products': products,
        # 'categories': Product.CATEGORY_CHOICES,
    })



def feature(request):
    return render(request, 'feature.html',  )



def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', )



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def generate_trnx_ref():
    rand_num = ''
    for i in range(10):
        rand_num += str(random.randint(0, 9))
    trnx_ref = 'TRNX-' + rand_num
    return trnx_ref
    

@api_view(['POST'])
@permission_classes([AllowAny])
def initiate_payment(request):
    try:
        if request.method == 'POST':
            amount = request.POST.get('amount')
            trnx_ref = generate_trnx_ref()
            user_id = request.POST.get('user_id')
            email = request.POST.get('email')
            url = 'https://api.flutterwave.com/v3/payments'
            headers = {
                "Content-Type": 'application/json',
                'Authorization': f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
               
            }
            data = {
                 'tx_ref': trnx_ref,
                "amount": amount,
                "currency": 'NGN',
                "redirect_url": request.build_absolute_uri('/payments/verify/'),
                
                "customer" : {
                    "email": email,
                    "phonenumber": '08027106648',
                    "name": email,
                },
                "customizations": {
                    "title": 'payment for Quiz',
                    "discription": 'Payment before writing a quize',
                    "Logo": "https://assets.piedpiper.com/logo.png",
                },
                "meta": {
                    "user_id": user_id,
                }
                
            }
            
            print(data['redirect_url'])
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = response.json()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
@api_view(['GET'])
def verify_payment(request):
    try:
        tx_ref = request.GET.get('tx_ref')
        tx_status = request.GET.get('Status')
        tranx_id = request.GET.get('transaction_id')
        
        url =  f"https://api.flutterwave.com/v3/transactions/{tranx_id}/verify"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer  {settings.FLUTTERWAVE_SECRET_KEY}",
            
            }
        response = requests.get(url, headers=headers)
        print(response)
        if response.status == 'success':
            print(response.data)
        else:
            print(response.message)
    except Exception as e:
        
        return Response({'error': f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        

class CustomLogin(auth_views.LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'

class CustomLogout(auth_views.LogoutView):
    next_page = reverse_lazy('home')  # redirect to home after logout