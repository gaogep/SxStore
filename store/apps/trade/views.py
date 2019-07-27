from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import mixins

from utils.permissions import IsOwnerOrReadOnly
from .serializer import SoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, OrderInfoDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """购物车功能开发"""
    serializer_class = SoppingCartSerializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializer
        else:
            return SoppingCartSerializer


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """订单功能开发"""
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderInfoDetailSerializer
        return OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_cart_records = ShoppingCart.objects.filter(user=self.request.user)
        for record in shop_cart_records:
            order_goods = OrderGoods()
            order_goods.goods = record.goods
            order_goods.goods_num = record.nums
            order_goods.order = order
            order_goods.save()
            record.delete()
        return order
