from django.shortcuts import render
from dashboard.models import Product, Category  # Use PascalCase for class names

def home(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'frontend/market/home.html', context=context)

def categoryDetails(request, pk):
    context = {}
    context['category'] = Category.objects.get(pk=pk)
    return render(request, 'frontend/market/category.html', context=context)

def ProductDetails(request, pk):
    context = {}
    context['product'] = Product.objects.get(pk=pk)
    return render(request, 'frontend/market/product.html', context=context)