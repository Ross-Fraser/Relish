import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.forms import OrderForm
from bag.models import BagItem
from roastery.models import CURRENCY_SYMBOLS

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
