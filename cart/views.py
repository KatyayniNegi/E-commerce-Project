from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product  # Adjust if your app/model name differs
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    cart_items = []
    grand_total = 0

    for product_id, item in cart.cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total = float(item['price']) * item['quantity']
            grand_total += total
            
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': total,
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'cart/detail.html', {
        'cart_items': cart_items,
        'total_price': grand_total,
    })
# Remove a product completely from the cart
def cart_remove(request, product_id):
    cart = Cart(request)
    product_id_str = str(product_id)
    if product_id_str in cart.cart:
        del cart.cart[product_id_str]
        cart.save()
    return redirect('cart:cart_detail')

# Decrease quantity by 1 (removes product if quantity reaches 0)
def cart_decrease(request, product_id):
    cart = Cart(request)
    product_id_str = str(product_id)
    if product_id_str in cart.cart:
        if cart.cart[product_id_str]['quantity'] > 1:
            cart.cart[product_id_str]['quantity'] -= 1
        else:
            del cart.cart[product_id_str]
        cart.save()
    return redirect('cart:cart_detail')