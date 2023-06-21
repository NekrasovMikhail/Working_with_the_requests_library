import requests

url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
resp = requests.get(url)
need_hero = ['Hulk', 'Captain America', 'Thanos']
powerstats_int = {}
for hero in need_hero:
    for heroes in resp.json():
        if heroes['name'] == hero:
            powerstats_int.update({hero: heroes['powerstats']['intelligence']})
print(f'Самый умный герой {[key for key, value in powerstats_int.items() if value == max(powerstats_int.values())][0]}')