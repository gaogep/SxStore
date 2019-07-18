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
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from .settings import MEDIA_ROOT
from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet, CategoryViewSet


router = DefaultRouter()
router.register('goods', GoodsListViewSet, base_name='goods')
router.register('categorys', CategoryViewSet, base_name='categorys')

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
    url('^', include(router.urls))
]
