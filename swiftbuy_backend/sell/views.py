import json
from unicodedata import category
from django.shortcuts import render
from http import HTTPStatus
from django.http import JsonResponse
from user.models import Product, Transaction, Wishlist, Notification, Brand, Category, Users
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np

# Create your views here.

def sellinfo(request):
    if request.user.is_authenticated:
        userid = request.user.uid
        products = Product.objects.filter(seller_id=userid)
        return JsonResponse({'status': 'success', 'results': list(products.values())}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)

@csrf_exempt
def addproduct(request):
    if request.user.is_authenticated:
        info = json.loads(request.body.decode('utf-8').replace("'", '"'))
        print(info)

        params = {
            'category': Category.objects.filter(category_id=info['category'])[0],
            'brand': info['brand'],
            'name': info['name'],
            'price': info['price'],
            'quantity_available': info['quantity'],
            'discount': info['discount'],
            'product_desc': info['productDesc'],
            'seller_id': request.user.uid,
            'images': info['image'],
            'advertised': info['advertised']
        }
        brandid = Brand.objects.filter(name=info['brand']).values('brand_id')
        if not brandid:
            Brand.objects.create(name=info['brand'])
            brandid = Brand.objects.filter(name=info['brand']).values('brand_id')[0]['brand_id']
        else:
            brandid = brandid[0]['brand_id']
        
        params['brand'] = Brand.objects.filter(brand_id=brandid)[0]
        # product = Product.objects.create(**{
        #     'category': params['category'], 'brand' : params['brand'],
        #     'name' : params['name'], 'price' : params['price'],
        #     'quantity_available' : params['quantity_available'],'discount' : params['discount'],
        #     'product_desc' : params['product_desc'],'seller' : params['seller'], 
        #     'images' : params['images'],'advertised' : params['advertised']
        #     })
       
        max_id = np.random.randint(25000, 100000)
        product = Product.objects.create(product_id=max_id, images=params['images'], category=params['category'], brand=params['brand'], name=info['name'], price=info['price'], quantity_available=info['quantity'], discount=info['discount'], product_desc=info['productDesc'], advertised=params['advertised'], seller_id=params['seller_id'])
        return JsonResponse({'results': product.product_id, 'status': 'success'}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)
        
def selling(request):
    if request.user.is_authenticated:
        userid = request.user.uid
        products = Product.objects.filter(seller_id=userid)
        return JsonResponse({'products': list(products.values()), 'status': 'success'}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)

def update(request, productid):
    if request.user.is_authenticated:
        info = json.loads(request.body.decode('utf-8').replace("'", '"'))
        userid = request.user.uid
        prev_quantity = Product.objects.filter(product_id=productid, seller_id=userid).values('quantity_available')[0]['quantity_available']
        if info['quantity_available'] > 0 and prev_quantity == 0:
            wishlist_users = list(Wishlist.objects.filter(product_id=productid).all().values('user_id'))
            Wishlist.objects.filter(product_id=productid).delete()
            for user in wishlist_users:
                Notification.objects.create(user_id=user['user_id'], product_id=productid, message="Your product is now available for purchase.", seen=0, timestamp=datetime.now())
            
        params = {
            'product_id': productid,
            'category': info['category'],
            'brand': info['brand'],
            'name': info['name'],
            'price': info['price'],
            'quantity_available': info['quantity_available'],
            'discount': info['discount'],
            'product_desc': info['product_desc']
        }
        Product.objects.filter(product_id=productid).update(**params)
        return JsonResponse({'status': 'success', 'results': 'Product updated'}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)

def delete(request, productid):
    if request.user.is_authenticated:
        userid = request.user.uid
        Product.objects.filter(product_id=productid, seller_id=userid).delete()
        return JsonResponse({'status': 'success', 'results': 'Product deleted'}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)

def history(request):
    if request.user.is_authenticated:
        userid = request.user.uid
        quantities = list(Transaction.objects.filter(seller_id=userid).values_list('product_id', 'quantity').order_by('product_id'))
        product_ids = [x[0] for x in quantities]
        products = list(Product.objects.filter(product_id__in=product_ids).values().order_by('product_id'))
        for i in range(len(quantities)) :
            products[i]['quantity'] = quantities[i][1]
        return JsonResponse({'status': 'success', 'results': products}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)

def analytics(request):
    if request.user.is_authenticated:
        userid = request.user.uid
        orders = list(Transaction.objects.filter(seller_id=userid).values('order_id'))
        past_week = Transaction.objects.filter(seller_id=userid, order_id__in=orders, orders__trasaction_time__gte=datetime.now() - timedelta(days=7))
        past_month = Transaction.objects.filter(seller_id=userid, order_id__in=orders, orders__trasaction_time__gte=datetime.now() - timedelta(days=30))
        past_year = Transaction.objects.filter(seller_id=userid, order_id__in=orders, orders__trasaction_time__gte=datetime.now() - timedelta(days=365))
        return JsonResponse({'status': 'success', 'past_week': list(past_week.values()), 'past_month': list(past_month.values()), 'past_year': list(past_year.values())}, status=HTTPStatus.OK)
    else:
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)
