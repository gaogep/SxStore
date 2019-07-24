from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializer import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        fields = ("user", "goods", "id")  # 如果要添加删除的功能 要将id放入

        # 由于这个validators不作用于单个字段之上,所以只能写在Meta信息中
        validators = [UniqueTogetherValidator(
            queryset=UserFav.objects.all(),
            fields=("user", "goods"),
            message="已经收藏"
        )]


class LeaveMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "id", "msg_type", "subject", "message", "file", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserAddress
        fields = ("user", "id", "province", "city", "district", "address", "signer_name", "signer_mobile", "add_time")
