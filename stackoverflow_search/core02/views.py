import requests
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from django.shortcuts import render
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator



class StackOverflow:
    base_url = "https://api.stackexchange.com/2.3/search"
    api_key = "<stackoverflow-api-key>" # paste your key here

    @classmethod
    def search(cls, query, page=1, page_size=5):
        params = {
            "site": "stackoverflow",
            "intitle": query,
            "page": page,
            "pagesize": page_size,
            "key": cls.api_key
        }
        response = requests.get(cls.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None


@api_view(['GET'])
@cache_page(60*60*24)
# @ratelimit(key='user', rate='5/m', block=True)
# @ratelimit(key='user', rate='100/d', block=True)
def search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    cache_key = f"stackoverflow_{query}_{page}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return Response(cached_response)
    else:
        response = StackOverflow.search(query, page=page)
        cache.set(cache_key, response, timeout=60*60*24)  # Cache for 24 hours
        print("------------------response------------------------------")
        return Response(response)


# http://localhost:8000/core02/search/?q=<your_query>&page=<page_number>