import json

from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
# from django.forms.models import model_to_dict
from django.core.serializers import serialize
# from django.views.generic import ListView

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        goods = Goods.objects.all()[:10]
        json_data = serialize('json', goods)
        return JsonResponse(json.loads(json_data), safe=False)


