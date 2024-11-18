from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from . models import Art, OrderItem, Order, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from django.db.models import Q
import requests


def art_list(request):
    query = request.GET.get('q')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_id = request.GET.get('category')  # Get selected category ID

    # Base query set
    art_list = Art.objects.all()

    # Apply search filter
    if query:
        art_list = art_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Apply price filters
    if price_min:
        art_list = art_list.filter(price__gte=price_min)
    if price_max:
        art_list = art_list.filter(price__lte=price_max)

    # Apply category filter if selected
    if category_id:
        art_list = art_list.filter(category_id=category_id)

    # Pass all categories to the template for the dropdown
    categories = Category.objects.all()
    return render(request, 'art/art_list.html', {
        'art_list': art_list,
        'categories': categories,
    })


def art_detail(request, art_id):
    art = get_object_or_404(Art, id=art_id)
    return render(request, 'art/art_detail.html', {'art': art})


def add_to_cart(request, art_id):
    cart = request.session.get('cart', {})
    cart[art_id] = cart.get(art_id, 0) + 1
    request.session['cart'] = cart
    return redirect('art:view_cart')


def remove_from_cart(request, art_id):
    cart = request.session.get('cart', {})
    art_id_str = str(art_id)
    if art_id_str in cart:
        del cart[art_id_str]
        request.session['cart'] = cart
    
    return redirect('art:view_cart')


def clear_cart(request):
    request.session['cart'] = {} 
    return redirect('art:art_list')


def view_cart(request):
    cart = request.session.get('cart', {})
    art_ids = cart.keys()
    artworks = Art.objects.filter(id__in=art_ids)
    cart_items = []
    for art in artworks:
        cart_items.append({
            'art': art,
            'quantity': cart[str(art.id)],
            'subtotal': art.price * cart[str(art.id)]
        })
    total = sum(item['subtotal'] for item in cart_items)
    return render(request, 'art/view_cart.html', {'cart_items': cart_items, 'total': total})



@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('art:view_cart')

    total_amount = 0
    for art_id, quantity in cart.items():
        art = Art.objects.get(id=art_id)
        total_amount += art.price * quantity

    # Create an order
    order = Order.objects.create(
        user=request.user,
        created_at=timezone.now(),
        total_amount=total_amount,
    )

    # Create order items
    for art_id, quantity in cart.items():
        art = Art.objects.get(id=art_id)
        OrderItem.objects.create(
            order=order,
            art=art,
            quantity=quantity,
            price=art.price,
        )

    # Clear the cart
    request.session['cart'] = {}

    return render(request, 'art/checkout_success.html', {'order': order})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'art/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Log the user in
            user = form.get_user()
            login(request, user)
            return redirect('art:art_list')  # Redirect to the art list page after login
    else:
        form = AuthenticationForm()

    return render(request, 'art/custom_login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('art:art_list')  # Redirect to the art list page after logout


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'art/order_history.html', {'orders': orders})

def about(request):
    return render(request, 'art/about.html')

def contact(request):
    return render(request, 'art/contact.html')