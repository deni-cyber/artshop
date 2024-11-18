from django.urls import path
from . import views

app_name = 'art'

urlpatterns = [
    path('', views.art_list, name='art_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('<int:art_id>/', views.art_detail, name='art_detail'),
    path('add_to_cart/<int:art_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'), 
    path('order_history/', views.order_history, name='order_history'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/remove/<int:art_id>/', views.remove_from_cart, name='remove_from_cart'),
]