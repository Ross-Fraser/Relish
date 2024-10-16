from .models import BagItem


def bag_items_count(request):
    total_items = 0
    if request.user.is_authenticated:
        bag_items = BagItem.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in bag_items)
    return {'bag_items_count': total_items}
