from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import  Http404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework.decorators import action
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ifsc_app.models import IFSC, ApiHistory
from ifsc_app.Serializers import ApiHistorySerializer, IFSCSerializer
import ifsc_app.db as db
from ifsc_app.logger import logger


                
#load excel data into sqlite3 in memory/file
db.load_in_memory()

def recordApi(endpoint="ifsc",ifsc=None):
    ApiHistory(ifsc=ifsc,endpoint=endpoint).save()

def payload(data, msg="success"):
    return {
        "details" : msg,
        "result" : data 
    }

class IFSCViewSet(viewsets.ModelViewSet):

    queryset = IFSC.objects.all()
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = LimitOffsetPagination
    serializer_class = IFSCSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, )    
    filterset_fields = [
        'city',
        'bank',
        'state',
        'district',
    ]
    search_fields = ("city", "bank",)

    def _filter(self, params, default_limit=10, default_sort='DESC'):
        limit =  default_limit
        sort = default_sort
        print(params)
        if 'fetchcount' in params:
            query_limit = params['fetchcount']
            limit = int(query_limit) if query_limit.isdigit() and int(query_limit) != 0 else default_limit
        
        if 'sortorder' in params:
            query_sort = params['sortorder']
            sort = query_sort if query_sort in ['ASC', 'DESC'] else default_sort
        return limit, sort

    @method_decorator(cache_page(settings.CACHE_TTL))
    def retrieve(self,request, pk=None):
        queryset = IFSC.objects.all()
        ifsc_data = {}
        try:
            ifsc_data = get_object_or_404(queryset, pk=pk)
        except Http404:
            return Response(payload(None,"Not found"),status=status.HTTP_404_NOT_FOUND)
        recordApi(endpoint="ifsc",ifsc=pk)
        serializer =  IFSCSerializer(ifsc_data)
        return Response(payload(serializer.data))

    @method_decorator(cache_page(settings.CACHE_TTL))
    @action(detail=False, methods=['get'])
    def leaderboard(self,request):
        params = self.request.query_params
        limit, sort = self._filter(params)
        result = IFSC.objects.values('bank').annotate(banks_count=Count('ifsc')).order_by(('' if sort == 'ASC' else '-') + 'banks_count')[:limit]
        if len(result) == 0:
            return Response(payload(None,"No banks found"))
        recordApi(endpoint="leaderboard")
        return Response(payload(result,"success"),status=200)

    @method_decorator(cache_page(settings.CACHE_TTL))
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        limit, sort = self._filter(self.request.query_params,default_limit=200, default_sort='ASC')
        queryset = ApiHistory.objects.exclude(ifsc__isnull=True).all().order_by(('' if sort == 'ASC' else '-') + 'timestamp')[:limit]
        if len(queryset) == 0:
            return Response(payload(None,"No History found"))
        recordApi(endpoint="statistics")
        serializer = ApiHistorySerializer(queryset,many=True)
        return Response(payload(serializer.data))

class ApiHistoryViewset(viewsets.ViewSet):

    permission_classes = [permissions.AllowAny]
    query_set = ApiHistory.objects.all()

    @action(detail=False, methods=['get'])
    def ifsc_hits(self, request):
        query_set = ApiHistory.objects.exclude(ifsc__isnull=True).values('ifsc').annotate(count=Count('timestamp')).order_by('ifsc')
        return Response(payload(query_set))
    
    @action(detail=False, methods=['get'])
    def api_hits(self, request):
        query_set = ApiHistory.objects.values('endpoint').annotate(count=Count('timestamp')).order_by('endpoint')
        return Response(payload(query_set))