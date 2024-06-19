from .models import category

def category_link(request):
    links = category.objects.all()
    return dict(links = links)
