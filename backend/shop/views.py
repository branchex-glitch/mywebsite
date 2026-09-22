from decimal import Decimal

from django.conf import settings
from django.contrib.auth import login, logout
from django.db import transaction
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem, Product
from .serializers import LoginSerializer, OrderItemInputSerializer, OrderSerializer, ProductSerializer, RegisterSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token(request):
    return Response({'csrfToken': get_token(request)})


@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    category = request.query_params.get('category')
    search = request.query_params.get('search')
    if category and category != 'all':
        products = products.filter(category=category)
    if search:
        products = products.filter(title__icontains=search)
    return Response(ProductSerializer(products, many=True).data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    login(request, user)
    return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response({'id': user.id, 'username': user.username})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({'id': request.user.id, 'username': request.user.username, 'email': request.user.email})


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    if not settings.GOOGLE_LOGIN_ENABLED:
        return Response({'detail': 'Google login is currently dormant.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'detail': 'Configure server-side Google token verification before enabling this endpoint.'}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    item_serializer = OrderItemInputSerializer(data=request.data.get('items', []), many=True)
    item_serializer.is_valid(raise_exception=True)
    items = item_serializer.validated_data
    if not items:
        return Response({'detail': 'At least one order item is required.'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        order = Order.objects.create(user=request.user, shipping_address=request.data.get('shipping_address', {}))
        total = Decimal('0.00')
        for item in items:
            product = Product.objects.get(pk=item['product_id'])
            unit_price = product.price
            OrderItem.objects.create(order=order, product=product, size=item['size'], quantity=item['quantity'], unit_price=unit_price)
            total += unit_price * item['quantity']
        order.total = total
        order.save(update_fields=['total'])

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    return Response(OrderSerializer(Order.objects.filter(user=request.user), many=True).data)
