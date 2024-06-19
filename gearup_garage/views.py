from django.shortcuts import render
from store.models import product, ProductImage

def home(request):
    products = product.objects.filter(is_active=True).order_by('-views')[:8]
    context = {
        'products': products
    }
    return render(request, 'index.html', context)