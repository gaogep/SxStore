"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.views.static import serve
from django.conf.urls import url, include
# from django.urls import path

# from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet
from users.views import UserViewSet
from user_opt.views import UserFavViewSet, LeaveMessageViewSet, AddressViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet
# from users.views import SendmsgViewSet


router = DefaultRouter()
router.register('goods', GoodsListViewSet, base_name='goods')
router.register('categorys', CategoryViewSet, base_name='categorys')
router.register('users', UserViewSet, base_name='users')
router.register('userfavs', UserFavViewSet, base_name='userfavs')
router.register('messages', LeaveMessageViewSet, base_name='messages')
router.register('address', AddressViewSet, base_name='address')
router.register('shopcarts', ShoppingCartViewSet, base_name='shopcarts')
router.register('orders', OrderViewSet, base_name='orders')
router.register('banners', BannerViewSet, base_name='banners')
router.register('indexGoods', IndexCategoryViewSet, base_name='indexGoods')

# router.register('code', SendmsgViewSet, base_name='code')

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list'
# })


urlpatterns = [
    url('^xadmin/', xadmin.site.urls),
    url('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 商品列表
    # url('^goods/', goods_list, name="goods-list"),

    # api文档
    url('^docs/', include_docs_urls(title="SxStore Docs")),

    # api调试 添加登录按钮
    url('^api-auth/', include('rest_framework.urls')),

    # router
    url('^', include(router.urls)),

    # drf自带的token验证
    # url(r'^api-token-auth/', views.obtain_auth_token)

    url(r'^login/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),

    # path('openapi', get_schema_view(
    #     title="SxStore",
    #     description="API for all things …"
    # ), name='openapi-schema'),

    # 第三方登录
    url('', include('social_django.urls', namespace='social'))
]
