import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import VerifyCode

User = get_user_model()
MOBILE_REGX = r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


class MsgSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:手机号码
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(MOBILE_REGX, mobile):
            raise serializers.ValidationError("手机号码不正确")

        # 验证发送频率
        one_minute = datetime.now() - timedelta(hours=0, minutes=1, seconds=1)
        if VerifyCode.objects.filter(mobile=mobile, add_time__gt=one_minute):
            raise serializers.ValidationError("距离上一次验证为超过60s")

        return mobile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "mobile", "code", "password")

    # write_only=True 不返回该字段
    code = serializers.CharField(write_only=True, required=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")

    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已经存在")])
    password = serializers.CharField(style={"input_type": "password"}, label="密码", write_only=True)

    # code只用于验证 不保存到数据库中 不返回值
    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("add_time")
        if verify_records:
            last_record = verify_records[0]
            if datetime.now() - last_record.add_time > timedelta(minutes=10):
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    # attrs每个字段validate之后返回的字典
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    # 设置密码
    # def create(self, validated_data):
    #     user = super().validated_data(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user
