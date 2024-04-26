from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("logout", views.logout_view, name="logout"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<int:category_id>", views.category_items_view, name="category_items_view"),
    path('load-more-items/', views.load_more_items, name='load_more_items'),
    path("item/<int:pk>", views.item_detail, name='item_detail'),
    path('add_to_favorite/<int:item_id>', views.add_to_favorite, name='add_to_favorite'),
    path('favorite', views.favorite_view, name='favorite_view'),
    path('add_to_cart/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('about', views.about_view, name='about_view'),
    path('questions', views.questions_view, name='questions_view'),
    path('search', views.search_view, name='search_view')

]
