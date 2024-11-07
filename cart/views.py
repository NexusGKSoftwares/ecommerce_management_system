# cart views
from django.shortcuts import render, redirect
from .models import CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required

def cart(request):
    items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart/cart.html', {'items': items})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart')
