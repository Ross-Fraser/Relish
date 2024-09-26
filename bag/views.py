from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BagItem
from roastery.models import CURRENCY_CHOICES, CURRENCY_SYMBOLS

@login_required
def bag_detail(request):
    bag_items = BagItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in bag_items)

    # Get the currency choices
    currency_choices = dict(CURRENCY_CHOICES)
    currency_symbols = dict(CURRENCY_SYMBOLS)

    # Get the selected currency from the request or use a default
    selected_currency = request.GET.get('currency', 'GBP')
    symbol = currency_symbols.get(selected_currency, '£')

    return render(request, 'bag_detail.html', {
        'bag_items': bag_items,
        'total_price': total_price,
        'currency_choices': currency_choices,
        'selected_currency': selected_currency,
        'symbol': symbol,
    })
