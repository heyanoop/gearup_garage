from django.shortcuts import render, get_object_or_404,redirect
from .models import product, ProductImage, Product_Variation
from categories.models import category
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.middleware.csrf import get_token

def store(request, category_slug=None):
    categories = None
    products = None
    images = None
    sort_by = request.GET.get('sort_by')
    
    if category_slug:
        categories = get_object_or_404(category, slug=category_slug)
        products = product.objects.filter(category=categories, is_active=True)
    else:
        products = product.objects.filter(is_active=True)
    
    if sort_by == 'nameas':
        products = products.order_by('product_name')
    elif sort_by == 'namedes':
        products = products.order_by('-product_name')
    elif sort_by == 'pricelh':
        products = products.order_by('price')
        
    elif sort_by == 'pricehl':
        products = products.order_by('-price')
    
        

    # Retrieve images related to the filtered products
    images = ProductImage.objects.filter(product__in=products)
    
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'images': images
    }
    return render(request, 'store/store.html', context)

def product_details(request, category_slug, product_slug):
    single_product = get_object_or_404(product, category__slug=category_slug, slug=product_slug)
    variations = Product_Variation.objects.filter(item = single_product)
    
    single_product.views += 1
    single_product.save()
    product_images = ProductImage.objects.filter(product=single_product)
    cat_offer = single_product.get_category_discount()
    prod_offer = single_product.get_product_offer()
    if cat_offer == 0 and prod_offer == 0:
        discount = 0
    elif cat_offer != 0:
        discount = cat_offer
    else:
        discount = prod_offer
    
    
    context = {
        'single_product': single_product,
        'product_images': product_images,
         'discount': discount,
         'variations': variations,
         'get_token': get_token,
        
         
    }

    return render(request, 'store/product_details.html', context)

def get_variant_stock(request, variation_id):
    if request.method == 'GET':
        try:
            variant = Product_Variation.objects.get(id=variation_id)
            return JsonResponse({'stock': variant.stock})
        except Product_Variation.DoesNotExist:
            return JsonResponse({'error': 'Variant not found'})
    else:
        return JsonResponse({'error': 'Invalid request'})





def product_search(request):
    keyword = request.GET.get('keyword', '')
    sort_by = request.GET.get('sort_by')

    all_products = product.objects.filter(is_active=True)

    if keyword:
        all_products = all_products.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

    if sort_by == 'name':
        all_products = all_products.order_by('product_name')
    elif sort_by == 'price':
        all_products = all_products.order_by('price')

    paginator = Paginator(all_products, 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    product_count = all_products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def price_range(request):
    if request.method == 'GET':
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        sort_by = request.GET.get('sort_by')
        
        filtered_products = product.objects.filter(price__gte=min_price, price__lte=max_price, is_active=True)
        
        if sort_by == 'name':
            filtered_products = filtered_products.order_by('product_name')
        elif sort_by == 'price':
            filtered_products = filtered_products.order_by('price')
        
        paginator = Paginator(filtered_products, 6)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
        product_count = filtered_products.count()
        
        context = {
            'products': paged_products,
            'product_count': product_count,
            'sort_by': sort_by,  # Pass the current sorting parameter to the template
        }
        return render(request, 'store/store.html', context)
    else:
        return redirect('store')