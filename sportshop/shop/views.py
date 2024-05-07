import random

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


from .models import User, Item, ItemImages, Categories, Watchlist, CartItem, Cart




def index(request):
    items = Item.objects.all()[:4]
    images = []
    pages = Item.objects.all()
    random_page = random.choice(pages)
    for item in items:

        first_image = ItemImages.objects.filter(item=item).first()
        if first_image:
                images.append(first_image)
    return render(request, 'index.html', {'items': items, 'images': images, 'random_page': random_page})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                    "message": "Username already taken."
            })
        login(request, user)
        Cart.objects.create(user=user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def categories_view(request):
    categories = Categories.objects.all()
    return render(request, 'categories.html', {'categories': categories})
def category_items_view(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
    items = Item.objects.filter(category=category)
    images = []
    for item in items:
        first_img = ItemImages.objects.filter(item=item).first()
        images.append(first_img)
    return render(request, 'category_items.html', {'items': items, 'category': category, "images": images})

def load_more_items(request):
    offset = int(request.GET.get('offset', 0))
    limit = 8
    items = Item.objects.all()[offset:offset+limit]
    data = []

    for item in items:
        item_detail_url = reverse('item_detail', args=[item.pk])
        first_image = ItemImages.objects.filter(item=item).first()
        image_url = first_image.image.url if first_image else ''

        data.append({
            'image': image_url,
            'name': item.name,
            'price': str(item.price),
            'created_at': item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'detail_url': item_detail_url
        })
    return JsonResponse(data, safe=False)
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    images = ItemImages.objects.filter(item=item)
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(item=pk, user=request.user).exists()
        return render(request, 'item_details.html', {"item": item, "images": images, "in_watchlist": in_watchlist})
    else:
        return render(request, 'item_details.html', {"item": item, "images": images})

def add_to_favorite(request, item_id):
    item = Item.objects.get(pk=item_id)
    user = request.user
    watchlist_item = Watchlist.objects.filter(user=user, item=item)
    if watchlist_item:
        watchlist_item.delete()
    else:
        watchlist = Watchlist.objects.create(user=user, item=item)
        watchlist.save()
    return redirect('item_detail', pk=item_id)
@login_required
def favorite_view(request):
    items = Watchlist.objects.filter(user=request.user)
    images = []
    for item in items:
        first_image = ItemImages.objects.filter(item=item.item).first()
        if first_image:
                images.append(first_image)
    return render(request, 'favorite.html', {'items': items, 'images': images})


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        quantity = request.POST.get('quantity')
        if quantity:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
                    cart_item.quantity += quantity
                    cart_item.item_price = item.price * quantity
                    cart_item.save()
                    cart.total_price += item.price * quantity
                    cart.save()
            except ValueError:
                pass

    return redirect('item_detail', pk=item_id)
@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    images = []
    for item in items:
        first_image = ItemImages.objects.filter(item=item.item).first()
        if first_image:
            images.append(first_image)
    return render(request, 'cart.html', {"items": items, "images": images, "cart": cart})
def remove_from_cart(request, pk):
    cart = Cart.objects.get(user=request.user)
    item = Item.objects.get(pk=pk)
    cart_obg = CartItem.objects.get(cart=cart, item=item)
    cart.total_price -= cart_obg.item_price
    cart.save()
    cart_obg.delete()

    return redirect('cart_view')
def about_view(request):
    return render(request, 'about.html')
def questions_view(request):
    return render(request, 'questions.html')
def search_view(request):
    query = request.GET.get('q')

    if query:
        results = Item.objects.filter(name__icontains=query)
        images = [ItemImages.objects.filter(item=item).first() for item in results]
    else:
        results = []
        images = []

    return render(request, 'search_results.html', {'results': results, 'query': query, 'images': images})



