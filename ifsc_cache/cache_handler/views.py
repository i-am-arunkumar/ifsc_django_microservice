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

def _fetch(url) :
    res = requests.get(url)
    res.raise_for_status()
    if(res.status_code == 200):
        return res.json()

def _get_or_set_cache(key,url,is_cache_hit=False):
    response = api_cache.get(key)
    if(response is None):
        response = _fetch(url)
        try:
            response = _fetch(url)
        except requests.exceptions.HTTPError as e:
            logger.error("database server is not running.")
            return {
                "result" : "Internal server error"
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
        api_cache.set(key,response)
        _increment_hit_count("api_" + key)
    else:
        _increment_hit_count(key)
    return response, status.HTTP_200_OK

@api_view(['GET',])
def ifsc(request, id):
    response, status = _get_or_set_cache(id,url_maps["ifsc"] + id)
    logger.debug("Hit counts : %s cache hits : %s, %s api hits %s",id,str(api_cache.get("hits_" + id)), id, str(api_cache.get("hits_api_" + id)))
    logger.info("%s -> %s", request.path_info, response.__str__())
    return Response(response,status=status)

@api_view(['GET'])
def leaderboard(request):
    response, status = _get_or_set_cache("leaderboard",url_maps["leaderboard"])
    logger.info("%s -> %s", request.path_info, response.__str__())
    return Response(response,status=status)
 
@api_view(['GET',])
def statistics(request):
    response, status = _get_or_set_cache("statistics",url_maps["statistics"])
    logger.info("%s -> %s", request.path_info, response.__str__())
    return Response(response,status=status)
