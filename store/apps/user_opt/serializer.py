from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


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
