from decimal import Decimal
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

    # Get currency information (similar to bag_detail)
    currency_symbols = dict(CURRENCY_SYMBOLS)
    selected_currency = request.GET.get('currency', 'GBP')
    symbol = currency_symbols.get(selected_currency, '£')

    # Prepare the order form
    order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'bag_items': bag_items,
        'total': total_prices,
        'delivery': delivery,
        'grand_total': grand_total,
        'symbol': symbol,
        'order_form': order_form,
    }

    return render(request, template, context)
