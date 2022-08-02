from  django.core.cache import cache as api_cache
from django.conf import settings

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.schemas import AutoSchema

import requests
from cache_handler.logger import logger

url_maps = {
    "ifsc" : "http://localhost:8000/api/ifsc/",
    "leaderboard" : "http://localhost:8000/api/ifsc/leaderboard",
    "statistics" : "http://localhost:8000/api/ifsc/statistics",
}

api_cache.clear()

def _increment_hit_count(key, prefix="hits_"):
    incr_key = prefix + key
    cur_count = api_cache.get_or_set(incr_key,0)
    api_cache.set(incr_key,int(cur_count) + 1)

def _fetch(url,params={}) :
    query_params = ""
    if(len(params) != 0):
        query_params = "?"
        for key,value in params.items():
            query_params += f"{key}={value}&" 
    logger.info("requesting : %s", url + query_params)
    res = requests.get(url + query_params)
    res.raise_for_status()
    if(res.status_code == 200):
        return res.json()

def _get_filter_suffix(request):
    filter_suffix = ""
    if request.GET is not None:
        for val in request.query_params.values():
            filter_suffix += "_" + val
    return filter_suffix

def _get_or_set_cache(key,url,params={}):
    response = api_cache.get(key)
    if(response is None):
        try:
            response = _fetch(url, params=params)
        except Exception as e:
            logger.error("main server is down/not reachable")
            return {
                "result" : "Internal server error"
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
        api_cache.set(key,response)
        _increment_hit_count("api_" + key)
    else:
        _increment_hit_count(key)
    return response, status.HTTP_200_OK

def _logs(id,url,response):
    logger.info("Hit counts : %s cache hits : %s, %s api hits %s",id,str(api_cache.get("hits_" + id)), id, str(api_cache.get("hits_api_" + id)))
    logger.debug("%s -> %s",url, response)

@api_view(['GET',])
def ifsc(request, id):
    response, status = _get_or_set_cache(id,url_maps["ifsc"] + id)
    _logs(id, request.path_info,response.__str__())
    return Response(response,status=status)

@api_view(['GET'])
def leaderboard(request):
    cache_key = "leaderboard" + _get_filter_suffix(request)
    response, status = _get_or_set_cache(
        cache_key,
        url_maps["leaderboard"])
    _logs(cache_key, request.path_info,response.__str__())
    return Response(response,status=status)
 
@api_view(['GET',])
def statistics(request):
    cache_key = "statistics" + _get_filter_suffix(request)
    response, status = _get_or_set_cache(
        cache_key,
        url_maps["statistics"], params=request.GET)
    _logs(cache_key, request.path_info,response.__str__())
    return Response(response,status=status)
