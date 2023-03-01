from django.shortcuts import render

from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.core.paginator import Paginator
import requests
import json

def search_stackoverflow(query):
    api_key = 'Q3)4V457HhT3ACgfyD)rsg(('
    base_url = 'https://api.stackexchange.com/2.3/search'
    params = {
        'site': 'stackoverflow',
        'intitle': query,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    questions = response.json()['items']
    return questions




@ratelimit(key='user', rate='5/s', block=True)
@ratelimit(key='user', rate='400/d', block=True)
def search(request):
    query = request.GET.get('q')
    page = int(request.GET.get('page', 1))
    print(page)
    if not query:
        return render(request, 'search.html')
    cache_key = f'stackoverflow_{query}'
    final_data = cache.get(cache_key)
    if not final_data:
        questions = search_stackoverflow(query)
        x = json.dumps(questions, indent=4)
        print(x)        
        paginator = Paginator(questions, 4)
        final_data = paginator.get_page(page)
        cache.set(cache_key, final_data, timeout=60*60*24) # Cache for 1 day
    context = {'questions': final_data}
    return render(request, 'search.html', context)


