from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_cart, name='get_cart'),              # GET /api/cart/
    path('add/', views.add_to_cart, name='add_to_cart'),    # POST /api/cart/add/
    path('item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),  # DELETE /api/cart/item/<id>/
]
