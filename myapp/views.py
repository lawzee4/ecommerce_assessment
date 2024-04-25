from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Book
from django.db.models import Q  # Import Q to perform complex queries
from django.http import JsonResponse  # Import JsonResponse for returning JSON data


def index(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def search(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter 'q'
    if query:
        books = Product.objects.filter(name__icontains=query) | Product.objects.filter(author__icontains=query)  # Case-insensitive search on title and author
        results = [{'name': book.name, 'image_url': book.image_url, 'price': book.price, 'author': book.author, 'rating': book.rating, 'release_date': book.release_date} for book in books]  # Prepare data for JSON response
    else:
        results = []  # Empty list if no query provided
    return render(request, 'search.html', {'books': results})


def login(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # Corrected redirection to 'index'
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
