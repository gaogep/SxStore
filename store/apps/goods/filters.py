from django_filters import rest_framework as filters
from .models import Goods


class GoodsFilter(filters.FilterSet):
    """商品的过滤器"""

    price_min = filters.NumberFilter(field_name='sale_price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='sale_price', lookup_expr='lte')
    goods_name = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'goods_name']
