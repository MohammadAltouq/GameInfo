import requests, requests_cache
from datetime import timedelta, date

requests_cache.install_cache('github_cache', backend='sqlite', expire_after=86400)

last_m = date.today()-timedelta(+60)
today = date.today()
tomorrow = date.today()+timedelta(1)
next_m = date.today()+timedelta(+180)

#filtering unwanted result
def tag_filter(data):
    tags_to_exclude = {"Erotic","erotica","porn","Sexual Content",  None}
    filtered_data = [game for game in data if not (game["tags"] is None or any(tag["name"] in tags_to_exclude for tag in game["tags"]))]
    # filtered_data = [game for game in data if not any(tag["name"] in tags_to_exclude for tag in game["tags"])]
    return filtered_data

# home page Api related calles
def f_rel():
    response = requests.get(f"https://api.rawg.io/api/games?key=d20c0eecee7c4c51960cb2489d65836b&dates={tomorrow},{next_m}&page_size=40&ordering=released")
    print (f'b_rel\ Used Cache: {response.from_cache}')
    data = response.json()
    return data["results"]

def n_rel():
    response = requests.get(f"https://api.rawg.io/api/games?key=d20c0eecee7c4c51960cb2489d65836b&dates={last_m},{today}&page_size=40&ordering=-released")
    print (f'b_rel\ Used Cache: {response.from_cache}')
    data = response.json()
    return data["results"]
    

def best_():
    response = requests.get("https://api.rawg.io/api/games?key=d20c0eecee7c4c51960cb2489d65836b&page_size=40&ordering=-metacritic")
    
    print (f'best_\ Used Cache: {response.from_cache}')
    data = response.json()
    return data["results"]

#search page API Calls
def abv_search(name,**kwargs):
    url = f'https://api.rawg.io/api/games?key=d20c0eecee7c4c51960cb2489d65836b'\
        f'&search={name}&dates={kwargs["start_year"]+"-01-01"},{kwargs["end_year"]+"-12-31"}&page_size={kwargs["page_size"]}'
    
    response = requests.get(url)
    print (f'sdv_search\ Used Cache: {response.from_cache}')
    data = response.json()
    return data["results"]

def basic_search(name):
        response = requests.get(f'https://api.rawg.io/api/games?key=d20c0eecee7c4c51960cb2489d65836b&page_size=40&search={name}')
        print (f'basic_search\ Used Cache: {response.from_cache}')
        data = response.json()
        return data["results"]

def detalis(rawg_id):
    response = requests.get(f'https://api.rawg.io/api/games/{rawg_id}?key=d20c0eecee7c4c51960cb2489d65836b')
    print (f'detalis\ Used Cache: {response.from_cache}')
    data = response.json()
    return data

def wt_buy(rawg_id):
    response = requests.get(f'https://api.rawg.io/api/games/{rawg_id}/stores?key=d20c0eecee7c4c51960cb2489d65836b')
    print (f'wt_buy\ Used Cache: {response.from_cache}')
    data = response.json()
    return data['results']

def screenshots(rawg_id):
    response = requests.get(f'https://api.rawg.io/api/games/{rawg_id}/screenshots?key=d20c0eecee7c4c51960cb2489d65836b')
    print (f'imgs\ Used Cache: {response.from_cache}')
    data = response.json()
    return data["results"]

def stores():
    response = requests.get(f'https://api.rawg.io/api/stores?key=d20c0eecee7c4c51960cb2489d65836b')
    print (f'stores data\ Used Cache: {response.from_cache}')
    data = response.json()
    return data["results"]

def get_detalis(rawg_id):
    data = detalis(rawg_id)
    data['short_screenshots'] = screenshots(rawg_id)
    data['wt_buy']= wt_buy(rawg_id)
    return data





