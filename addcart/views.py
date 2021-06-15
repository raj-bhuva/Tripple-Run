from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from idesign.models import Web
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.http import HttpResponseRedirect, JsonResponse


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Web.objects.get(id=id)
    cart.add(product=product)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Web.objects.get(id=id)
    cart.remove(product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Web.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Web.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
