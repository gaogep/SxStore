from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(filters.FilterSet):
    """商品的过滤器"""

    pricemin = filters.NumberFilter(field_name='sale_price', lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name='sale_price', lookup_expr='lte')
    goods_name = filters.CharFilter(field_name='name', lookup_expr='contains')
    top_category = filters.NumberFilter(method='top_category_filter')

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'goods_name', 'is_hot']

    # 根据商品1级类目id找出下面的所有商品
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) |
                               Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))
