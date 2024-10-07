from django.urls import path
from . import views

app_name = 'bag'

urlpatterns = [
    path('', views.bag_detail, name='bag_detail'),
    path('add/<int:product_id>/', views.add_to_bag, name='add_to_bag'),
    path('update/<int:item_id>/', views.update_bag_item, name='update_bag_item'),
    path('remove/<int:item_id>/', views.remove_from_bag, name='remove_from_bag'),
]
