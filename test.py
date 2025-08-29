import httpx

API_KEY = "RGAPI-abd9cacd-b224-41d1-9def-8c0c43ec82b3"
PLATFORM = "EUROPE" 
REGION = "EUN1"
gameName = "Gowi"
tagLine = "420"

def get_puuid(gameName, tagLine, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200: 
        return response.json().get("puuid")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_match_history(puuid, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_match_details(match_id, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

puuid = get_puuid(gameName, tagLine, PLATFORM, API_KEY)
print(f"PUUID: {puuid}")

match_history = get_match_history(get_puuid(gameName, tagLine, PLATFORM, API_KEY), PLATFORM, API_KEY)
print(match_history)