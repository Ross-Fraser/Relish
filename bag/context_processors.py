from bag.models import BagItem

def bag_items_count(request):
    if request.user.is_authenticated:
        return {
            'bag_items_count': BagItem.objects.filter(user=request.user).count()
        }
    return {'bag_items_count': 0}
