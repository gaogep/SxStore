from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import filters
# from rest_framework.authentication import TokenAuthentication

from .models import Goods, GoodsCategory
from .serializer import GoodsSerializer, CategorySerializer
from .filters import GoodsFilter


class GoodsListViewDrfVersion1(APIView):
    """显示10条商品"""
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        goods_serializer = GoodsSerializer(data=request.data)
        if goods_serializer.is_valid():
            goods_serializer.save()
            return Response(goods_serializer.data, status=status.HTTP_201_CREATED)
        return Response(goods_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GoodsListViewDrfVersion2(mixins.ListModelMixin, generics.GenericAPIView):
    """商品列表页"""
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewDrfVersion3(generics.ListAPIView):
    """商品列表页"""
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # authentication_classes = (TokenAuthentication,)
    pagination_class = GoodsPagination
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'category__name')
    ordering_fields = ('sold_nums', 'sale_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
