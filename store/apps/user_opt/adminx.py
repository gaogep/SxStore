import xadmin

from .models import *


class UserFavAdmin:
    list_display = ['user', 'goods', 'add_time']
    list_filter = ['user__name', 'goods__name']
    search_fields = ['user', 'goods']


class UserLeavingMessageAdmin:
    list_display = ['user', 'msg_type', 'subject']
    list_filter = ['user__name', 'subject']
    search_fields = ['user', 'subject', 'message']


class UserAddressAdmin:
    list_display = ['user', 'province', 'city', 'district', 'signer_name', 'signer_mobile', 'add_time']
    list_filter = ['user__name', 'province', 'city', 'district', 'signer_name', 'signer_mobile']
    search_fields = ['user', 'province', 'city', 'district', 'signer_name', 'signer_mobile']


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
