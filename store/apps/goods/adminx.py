import xadmin

from .models import *


class GoodsAdmin:
    list_display = ['name', 'click_nums', 'click_nums', 'fav_nums',
                    'sold_nums', 'goods_inventory', 'market_price', 'sale_price',
                    'goods_brife_intro', 'ship_free', 'is_new', 'is_hot', 'add_time']
    list_filter = ['category__name', 'goods_sn', 'name', 'click_nums', 'click_nums', 'fav_nums',
                   'sold_nums', 'goods_inventory', 'market_price', 'sale_price',
                   'goods_brife_intro', 'ship_free', 'is_new', 'is_hot']
    list_editable = ['is_new', 'is_hot']
    search_fields = ['goods_sn', 'name']


class GoodsCategoryAdmin:
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["parent_category__name", "category_type", "name",]
    search_fields = ['name']


class GoodsCategoryBrandAdmin:
    list_display = ["category", "image", "name", "brife_intro"]


class GoodsDetailBannerAdmin:
    list_display = ["goods", "image", "add_time"]


class IndexBannerAdmin:
    list_display = ["goods", "image", "index", "add_time"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsCategoryBrandAdmin)
xadmin.site.register(GoodsDetailBanner, GoodsDetailBannerAdmin)
xadmin.site.register(IndexBanner, IndexBannerAdmin)
