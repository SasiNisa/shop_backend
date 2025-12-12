""" from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from products.models import Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, created = Cart.create(user=request.user)
    items = cart.items.values('product__id', 'product__name', 'quantity', 'product__price')
    return Response({"items": list(items), "total": cart.total_price})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += int(quantity)

    cart_item.save()
    return Response({"message": "Item added to cart"})
 """


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart, CartItem
from products.models import Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    cart_data = [
        {
            "id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": float(item.product.price),
            "total_price": float(item.total_price)
        } for item in items
    ]
    return Response({"items": cart_data, "total": float(cart.total_price)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += quantity

    cart_item.save()
    return Response({"message": "Item added to cart"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    cart_item.delete()
    return Response({"message": "Item removed"})

