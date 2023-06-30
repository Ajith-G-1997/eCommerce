from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, AdminLoginForm, LoginForm, PostForm
from django.contrib.auth.forms import UserCreationForm
from .models import AddProduct, CartItem,UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST


# ------------------------Display the Index page Function---------------------------------------
def index(request):
    return render(request, 'base.html')


# ------------------------End Display the Index page Function---------------------------------------


# --------------------------- Admin Login section -------------------------------
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if username == 'admin' and password == 'admin@123':
                return render(request, 'admin/dashboard.html')
            else:
                error_message = "Invalid username or password."
                return render(request, 'admin/login.html', {'form': form, 'error_message': error_message})
    else:
        form = AdminLoginForm()

    return render(request, 'admin/login.html', {'form': form})


# ---------------------------  End Admin Login section --------------------------------------------------


# ------------------------Home Page User Sign in And Sign Up Functions --------------------------------
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import LoginForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('customer_view')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})





# ------------------------ End Home Page User Sign in And Sign Up Functions --------------------------------


# ---------------------------------Admin Panel Functions--------------------------------------------------
def admin_dashboard(request):
    return render(request, 'admin/admin_base.html')


def add_product(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('Product_List')
    else:
        form = PostForm()
    return render(request, 'admin/add_product.html', {'form': form})


def Product_List(request):
    products = AddProduct.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(AddProduct, pk=pk)
    return render(request, 'admin/product_detail.html', {'product': product})


def product_update(request, pk):
    post = get_object_or_404(AddProduct, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('Product_List',)
    else:
        form = PostForm(instance=post)
    return render(request, 'admin/product_update.html', {'form': form})


def product_delete(request, pk):
    post = get_object_or_404(AddProduct, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('Product_List')
    return render(request, 'admin/product_delete.html', {'post': post})


def customer_list_view(request):
    customers = User.objects.all()
    return render(request, 'admin/customer_list.html', {'customers': customers})


# --------------------------------------End Admin Panel Functions --------------------------------------------


# --------------------------------------User Panel Functions----------------------------------------------------
def customer_view(request):
    return render(request, 'customer/dashboard.html')


def customer_product_list(request):
    products = AddProduct.objects.all()
    return render(request, 'customer/product_list.html', {'products': products})


def add_to_cart_view(request, pk):
    products = AddProduct.objects.all()

    # For cart counter, fetching product IDs added by the customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 1

    response = render(request, 'customer/product_list.html', {'products': products, 'product_count_in_cart': product_count_in_cart})

    
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids == "":
            product_ids = str(pk)
        else:
            product_ids = product_ids + "|" + str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product = AddProduct.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')

    return response

def cart_view(request):
    # for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # fetching product details from db whose id is present in cookie
    products = None
    total = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart = [pid for pid in product_ids.split('|') if pid]

            if product_id_in_cart:
                products = AddProduct.objects.filter(id__in=product_id_in_cart)

                # for total price shown in cart
                for p in products:
                    total += p.price

    return render(request, 'customer/cart.html', {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})




def remove_from_cart_view(request, pk):
    # Retrieve product IDs from the cookie
    product_ids = request.COOKIES.get('product_ids', '').split('|')
    product_ids = list(filter(None, product_ids))  # Remove empty strings

    # Ensure that pk is a valid integer
    try:
        pk = int(pk)
    except ValueError:
        # Handle the case when pk is not a valid integer
        return HttpResponse("Invalid product ID")

    # Remove the specified product ID from the cart
    if str(pk) in product_ids:
        product_ids.remove(str(pk))

    # Retrieve products with remaining IDs
    products = AddProduct.objects.filter(id__in=product_ids)

    # Calculate total price
    total = sum(p.price for p in products)

    # Update the cookie with the modified product IDs
    value = '|'.join(product_ids)
    response = render(request, 'customer/cart.html', {'products': products, 'total': total, 'product_count_in_cart': len(product_ids)})
    if value == '':
        response.delete_cookie('product_ids')
    else:
        response.set_cookie('product_ids', value)

    return response




def profile(request):
    return render(request,'customer/my_profile.html')