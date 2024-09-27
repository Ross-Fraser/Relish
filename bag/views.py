from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BagItem
from roastery.models import Product
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
    
@login_required
def add_to_bag(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    bag_item, created = BagItem.objects.get_or_create(user=request.user, product=product)
    
    if created:
        bag_item.quantity = 1
    else:
        bag_item.quantity += 1
        
    bag_item.save()
    return redirect('bag:bag_detail')

@login_required
def update_bag_item(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        item = get_object_or_404(BagItem, id=item_id)
        item.quantity = int(quantity)
        item.save()
    
    return redirect('bag:bag_detail')

@login_required
def remove_from_bag(request, item_id):
    bag_item = get_object_or_404(BagItem, id=item_id, user=request.user)
    bag_item.delete()
    return redirect('bag:bag_detail')

