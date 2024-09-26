from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BagItem
from roastery.models import Product

@login_required
def bag_detail(request):
    bag_items = BagItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in bag_items)
    return render(request, 'bag_detail.html', {'bag_items': bag_items, 'total_price': total_price})