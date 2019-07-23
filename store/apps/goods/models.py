from datetime import datetime

from django.db import models


class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(max_length=30, verbose_name="类名", default="", help_text="类名")
    code = models.CharField(max_length=30, verbose_name="类别码", default="", help_text="类别码")
    brife_intro = models.CharField(max_length=200, verbose_name="简单描述", default="", help_text="简单描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类", on_delete=models.CASCADE,
                                        related_name="sub_cat", help_text="父类")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类别", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, verbose_name="品牌名", default="", help_text="品牌名")
    brife_intro = models.CharField(max_length=200, verbose_name="品牌描述", default="", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to='brands', verbose_name="品牌图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类别", on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name="商品名", default="", help_text="商品名")
    goods_sn = models.CharField(max_length=200, verbose_name="商品编码", default="", help_text="商品编码")
    click_nums = models.IntegerField(default=0, verbose_name="商品点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="商品收藏数")
    sold_nums = models.IntegerField(default=0, verbose_name="商品卖出数量")
    goods_inventory = models.IntegerField(default=0, verbose_name="商品库存")
    market_price = models.FloatField(default=0, verbose_name="商品市场价")
    sale_price = models.FloatField(default=0, verbose_name="商品售价")
    goods_brife_intro = models.TextField(max_length=500, default="", verbose_name="商品简介")
    goods_desc = models.TextField(max_length=1000, default="", verbose_name="商品详情")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    ship_free = models.BooleanField(default=False, verbose_name="是否免运费")
    goods_front_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name="商品封面图片")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热卖")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsDetailBanner(models.Model):
    """
    商品详情内部的轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品名", on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(max_length=200, upload_to='goods_detail_banner', verbose_name="商品轮播图")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品详情页轮播图"
        verbose_name_plural = verbose_name


class IndexBanner(models.Model):
    """
    首页的轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='index_banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '首页商品轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

