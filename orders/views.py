# orders views
from django.shortcuts import render, redirect
from .models import Order
from cart.models import CartItem
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            total_amount=total,
        )

        # Mark cart items as ordered (optional)
        items.delete()
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'orders/checkout.html', {'items': items, 'total': total})

@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_confirmation.html', {'order': order})
