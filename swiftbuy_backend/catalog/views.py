from http import HTTPStatus
from urllib.request import Request
from django.shortcuts import render
from django.http import JsonResponse
from user.models import Category, Product
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
# @csrf_exempt
def categories(request):
    # print(request.user.is_authenticated)
    print("ATLEAST here")
    if request.user.is_authenticated:
        print("NOT SO SAD")
        categories = Category.objects.all()
        return JsonResponse({'status': 'success', 'results': list(categories.values())}, status=HTTPStatus.OK)
    else :
        print("SAD")
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)

def products(request, categoryid):
    if request.user.is_authenticated:
        products = list(Product.objects.filter(category_id=categoryid).values())
        for p in products :
            p['images'] = p['images'][1:-1].replace('\\', '').split(',')[0]
        return JsonResponse({'status': 'success', 'results': products}, status=HTTPStatus.OK)
    else :
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)
 
def viewproduct(request, productid):
    if request.user.is_authenticated:
        product = Product.objects.filter(product_id=productid).values()[0]
        return JsonResponse({'status': 'success', 'results': product}, status=HTTPStatus.OK)
    else :
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)

def search(request):
    if request.user.is_authenticated:
        query = json.loads(request.body.decode('utf-8').replace("'", '"'))['query']
        products = Product.objects.filter(name__icontains=query).filter(product_desc__icontains=query)
        return JsonResponse({'status': 'success', 'results': list(products.values())}, status=HTTPStatus.OK)
    else :
        return JsonResponse({'status': 'auth_failure', 'results': 'User not authenticated'}, status=HTTPStatus.UNAUTHORIZED)