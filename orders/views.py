from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Order, OrderItem
from cart.cart import Cart

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            pincode=request.POST.get('pincode'),
            total_amount=cart.get_total_price()
        )
        for item_id, item_data in cart.cart.items():
            OrderItem.objects.create(
                order=order,
                product_id=item_id,
                price=Decimal(item_data['price']),
                quantity=item_data['quantity']
            )
        request.session['cart_session'] = {}  # Clear cart
        return redirect('orders:order_history')
        
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})