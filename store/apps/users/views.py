from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.response import Response
# from rest_framework import status

from .serializer import RegisterSerializer
# from .serializers import MsgSerializer
# from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    """重载用户登录的验证方法"""
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# class SendmsgViewSet(CreateModelMixin, viewsets.GenericViewSet):
#     """接收用户发送来的手机号码，验证后发送短信验证码"""
#     serializer_class = MsgSerializer
#
#     # 生成验证码
#     def generate_code(self):
#         seeds = "1234567890"
#         rdm_str = []
#         for i in range(4):
#             rdm_str.append(random.choice(seeds))
#         return "".join(rdm_str)
#
#     def create(self, request, *args, **kwargs):
#         # 验证手机号码
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         获取通过验证的手机号码
#         mobile = serializer.validated_data['mobile']
#         code = self.generate_code()
#         在这里写发送短信的代码 ret = send_msg(mobile, code ...) ...
#
#         if ret["code"] != 0:
#             return Response({
#                 "mobile": ret["msg"]
#             }, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             code_record = VerifyCode(code=code, mobile=mobile)
#             code_record.save()
#             return Response({
#                 "mobile": mobile
#             }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    # 重载create和perform_create方法,实现注册后自动登录
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        refresh = RefreshToken.for_user(user)

        # 生成令牌并添加至返回的数据中
        serializer.data["refresh"] = str(refresh)
        serializer.data["Bearer"] = str(refresh.access_token)

        # 添加username至返回的数据中
        serializer.data["username"] = user.username if user.username else user.name

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # serializer是RegisterSerializer中Meta里的Model对象
    def perform_create(self, serializer):
        return serializer.save()
