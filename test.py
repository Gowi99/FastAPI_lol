import httpx

API_KEY = "RGAPI-0cc0880e-d04d-4ee8-83cb-a085234aa079"
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

def get_gameName_and_tagLine_from_puuid(puuid, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("gameName"), data.get("tagLine")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None

puuid = get_puuid(gameName, tagLine, PLATFORM, API_KEY)
print(f"PUUID: {puuid}")

match_history = get_match_history(get_puuid(gameName, tagLine, PLATFORM, API_KEY), PLATFORM, API_KEY)
print(match_history)

praticipants = get_match_details(match_history[0], PLATFORM, API_KEY)['metadata']['participants']
print(len(praticipants))

for puuid in praticipants:
    gameName, tagLine = get_gameName_and_tagLine_from_puuid(puuid, PLATFORM, API_KEY)
    print(f"{gameName}#{tagLine}")


