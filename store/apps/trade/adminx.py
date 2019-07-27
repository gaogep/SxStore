import xadmin

from .models import *


class ShoppingCartAdmin:
    list_display = ['user', 'goods', 'nums', 'add_time']
    list_filter = ['user__name']
    search_fields = ['user']


class OrderInfoAdmin:
    list_display = ['user', 'order_sn', 'trade_no', 'pay_status', 'order_mount',
                    'pay_time', 'post_script', 'address', 'signer_name', 'signer_mobile', 'add_time']
    list_filter = ['user__name', 'order_sn', 'trade_no']
    search_fields = ['user']


class OrderGoodsAdmin:
    list_display = ['order', 'goods', 'goods_num', 'add_time']
    list_filter = ['order__order_sn', 'goods__name', 'goods_num']
    search_fields = ['order']


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderGoods, OrderGoodsAdmin)
