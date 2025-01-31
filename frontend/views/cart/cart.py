from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from frontend.models.cart import Cart, CartItem
from frontend.models.customer import Customer
from dashboard.models.product import Product
import uuid

def get_or_create_cart(request):
    """
    Helper function to get or create a cart for the current user (authenticated or anonymous).
    """
    if request.user.is_authenticated:
        # For authenticated users, link the cart to the Customer
        customer, created = Customer.objects.get_or_create(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
    else:
        # For anonymous users, use the session ID
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        customer, created = Customer.objects.get_or_create(session_id=session_id)
        cart, created = Cart.objects.get_or_create(customer=customer)
    return cart

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

    cart = get_or_create_cart(request)  # Use the helper function to get or create the cart

    # Add or update the product in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        'success': True,
        'message': _(f'{quantity} x {product.name} added to cart.'),
    })

@require_POST
def update_cart_item(request, cart_item_id):
    """
    Update the quantity of a specific cart item.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        message = f'Updated {cart_item.product.name} quantity to {quantity}.'
    else:
        cart_item.delete()
        message = f'{cart_item.product.name} removed from cart.'

    return JsonResponse({
        'success': True,
        'message': message,
    })

@require_POST
def remove_from_cart(request, cart_item_id):
    """
    Remove a specific cart item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    product_name = cart_item.product.name
    cart_item.delete()

    return JsonResponse({
        'success': True,
        'message': f'{product_name} removed from cart.',
    })

def view_cart(request):
    """
    Display the contents of the cart.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()  # Get all items in the cart

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)