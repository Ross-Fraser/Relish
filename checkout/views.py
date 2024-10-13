import stripe
from decimal import Decimal
import json
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from checkout.forms import OrderForm
from django.views.decorators.http import require_POST
from bag.models import BagItem
from roastery.models import CURRENCY_SYMBOLS
from checkout.models import Order, OrderLineItem

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)

@login_required
def checkout(request):
    bag_items = BagItem.objects.filter(user=request.user)
    if not bag_items:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('home'))

    total_prices = sum(item.get_total_price() for item in bag_items)
    delivery = Decimal('5.00') if total_prices > 0 else Decimal('0.00')
    grand_total = total_prices + delivery

    # Get currency information
    currency_symbols = dict(CURRENCY_SYMBOLS)
    selected_currency = request.GET.get('currency', 'GBP')
    symbol = currency_symbols.get(selected_currency, '£')

    # Set up Stripe payment
    stripe.api_key = settings.STRIPE_SECRET_KEY
    amount_in_cents = int(grand_total * 100)

    intent = stripe.PaymentIntent.create(
        amount=amount_in_cents,
        currency=selected_currency.lower(),
        payment_method_types=['card'],
    )

    if request.method == 'POST':
        form_data = {
            'first_name': request.POST.get('first_name', ''),
            'surname': request.POST.get('surname', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'county': request.POST.get('county', ''),
            'postcode': request.POST.get('postcode', ''),
            'country': request.POST.get('country', ''),          
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Save the order
            order = order_form.save(commit=False)
            order.stripe_pid = intent.id
            order.original_bag = bag_items
            order.save()

            # Create order line items
            for item in bag_items:
                order_line_item = OrderLineItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    product_size=item.size,
                )
                order_line_item.save()

            # Clear the user's bag
            BagItem.objects.filter(user=request.user).delete()

            # Redirect to the checkout success page
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

    if request.user.is_authenticated:
        initial_data = {
            'first_name': request.user.first_name,
            'surname': request.user.last_name,
            'email': request.user.email,
        }
        order_form = OrderForm(initial=initial_data)
    else:
        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'bag_items': bag_items,
        'total': total_prices,
        'delivery': delivery,
        'grand_total': grand_total,
        'symbol': symbol,
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
