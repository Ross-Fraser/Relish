from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .forms import ProductForm
from django.views import generic
from .models import Product, CONTINENT_CHOICES
from django.db.models import Q


def index(request):
    continents = [
        {'name': 'African', 'continent_index': 0},
        {'name': 'Asian', 'continent_index': 1},
        {'name': 'American', 'continent_index': 2},
    ]

    continent_list = []
    for continent in continents:
        image = get_continent_image(continent['continent_index'])
        continent_list.append({'name': continent['name'], 'image': image})

    return render(request, 'index.html', {'continent_list': continent_list})


def get_continent_image(continent_index):
    continent_images = {
        0: 'Relish-Coffee-Africa-Selection-300x300.webp',
        1: 'Relish-Coffee-Asian-Selection-300x300.webp',
        2: 'Relish-Coffee-American-Selection-300x300.webp'
    }

    return continent_images.get(continent_index,)


class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = "roastery/index.html"
    paginate_by = 6


from django.db.models import Q

def products_list(request):
    query = request.GET.get('q', '')
    continent_filter = request.GET.get('continent', '')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if continent_filter:
        products = products.filter(origin__continent=int(continent_filter))

    continent_choices = dict(CONTINENT_CHOICES)

    context = {
        'products': products,
        'query': query,
        'continent_filter': continent_filter,
        'continents': continent_choices,
    }
    return render(request, 'roastery/products_list.html', context)



def origin_products(request, continent_name=None):

    if not continent_name:
        return render(request, 'origin_products.html', {
        })

    continent_index = next((index for index, name in CONTINENT_CHOICES
                            if name == continent_name), None)
    if continent_index is None:
        products = []
    else:
        products = Product.objects.filter(origin__continent=continent_index)

    return render(request, 'origin_products.html', {
        'products': products,
        'continent_name': continent_name
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    currency_symbol = product.get_currency_symbol()
    success_message = request.GET.get('success_message')

    context = {
        'product': product,
        'continent_name': product.origin.get_continent_display(),
        'country_name': product.origin.get_country_display(),
        'currency_symbol': currency_symbol,
        'success_message': success_message,
    }
    return render(request, 'product_detail.html', context)


@login_required
@permission_required('roastery.add_product', raise_exception=True)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'{reverse("manage_products")}?'
                            f'success_message=Product created successfully!')
        else:
            return render(request, 'roastery/product_form.html',
                          {'form': form})
    else:
        form = ProductForm()

    return render(request, 'roastery/product_form.html', {'form': form})


@login_required
@permission_required('roastery.manage_products', raise_exception=True)
def manage_products(request):
    products = Product.objects.all()
    success_message = request.GET.get('success_message', None)
    return render(request, 'roastery/manage_products.html',
                  {'products': products, 'success_message': success_message})


@login_required
@permission_required('roastery.change_product', raise_exception=True)
def update_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('manage_products') +
                            '?success_message=Product updated successfully!')

    else:
        form = ProductForm(instance=product)

    success_message = request.GET.get('success_message')

    return render(request, 'roastery/product_form.html', {'form': form,
                                                          'success_message':
                                                              success_message})


@login_required
@permission_required('roastery.delete_product', raise_exception=True)
def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect(f'{reverse("manage_products")}?'
                        f'success_message=Product deleted successfully!')
    else:
        return JsonResponse({'success': False}, status=400)


def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)
