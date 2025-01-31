from frontend.models.order import Order, OrderItem
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from frontend.views.cart.cart import get_or_create_cart

@require_POST
def save_shipping_details(request):
    """
    Save shipping details to the order and proceed to payment.
    """
    # Get the current cart
    cart = get_or_create_cart(request)

    # Validate the form data
    full_name = request.POST.get('full-name')
    address = request.POST.get('address')
    city = request.POST.get('city')
    country = request.POST.get('country')
    errors = {}

    if not all([full_name, address, city, country]):
        errors['shipping_details'] = _('Please fill out all shipping details.')

    if errors:
        return JsonResponse({'success': False, 'errors': errors})
    # Create a new order with shipping details
    try:
        order = Order.objects.create(
            customer=cart.customer,
            full_name=full_name,
            address=address,
            city=city,
            country=country,
            total_price=cart.total_price + 20,  # Calculate the total price from the cart
        )

        # Add cart items to the order
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

        # Clear the cart after creating the order
        cart.items.all().delete()

        return JsonResponse({
            'success': True,
            'message': _('Shipping details saved successfully.'),
            'redirect_url': '/cart/',  # Redirect to the payment page
        })
    except Exception as e:

        return JsonResponse({
            'success': False,
            'errors': {
                'shipping_details': _(f'Failed to save shipping details {str(e)}'),},
        })