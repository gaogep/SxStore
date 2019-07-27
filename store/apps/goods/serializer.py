from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Goods, GoodsCategory, GoodsDetailBanner, IndexBanner, GoodsCategoryBrand

User = get_user_model()


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)  # many=True表示下面有多个三类

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)  # many=True表示下面有多个二类

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsDetailBanner
        fields = ("image", )


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = GoodsImageSerializer(many=True)
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = Goods
        fields = "__all__"

    def create(self, validated_data):
        return Goods.objects.create(**validated_data)


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndexBanner
        fields = "__all__"


class BrandSerialzier(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexGoodsSerializer(serializers.ModelSerializer):
    brands = BrandSerialzier(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(
            Q(category_id=obj.id) |
            Q(category__parent_category_id=obj.id) |
            Q(category__parent_category__parent_category_id=obj.id)
        )
        return GoodsSerializer(all_goods, many=True).data
