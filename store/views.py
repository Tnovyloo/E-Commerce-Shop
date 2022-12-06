from django.shortcuts import render
from store.models import Product

# Create your views here.

def store(request):
    products = Product.objects.all()

    context = {'products': products}

    return render(request, template_name='store/store.html', context=context)

