from django.contrib import admin
from .models import Category, CoffeeOrigin, CoffeeGrind, CoffeeSize, Product
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):

    list_display = ('name', 'slug', 'price')
    search_fields = ['name', 'description']
    summernote_fields = ('description',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'origin', 'grind', 'size')


# Register your models here.
admin.site.register(Category)
admin.site.register(CoffeeOrigin)
admin.site.register(CoffeeGrind)
admin.site.register(CoffeeSize)
