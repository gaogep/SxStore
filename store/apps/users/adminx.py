import xadmin
from xadmin import views

from .models import *


class GlobalSetting:
    site_title = '生鲜商城后台管理系统'
    site_footer = '生鲜网'
    menu_style = 'accordion'


class UserProfileAdmin:
    list_display = ['username', 'name', 'birthday', 'gender', 'mobile', 'email']
    list_filter = ['username', 'name', 'birthday', 'gender', 'email']
    search_fields = ['username', 'name', 'mobile', 'email']


class VerifyCodeAdmin:
    list_display = ['code', 'mobile', 'add_time']
    list_filter = ['code', 'mobile']
    search_fields = ['code', 'mobile']


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)
