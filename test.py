from config import API_KEY
import httpx
from datetime import datetime, timedelta


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
        return response.json()  # pytanie czy my chcemy całego jsona czy tylko jakąś jego część, bo szkoda zapytań
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

# Pobieranie zawodników z historii meczów

praticipants = get_match_details(match_history[0], PLATFORM, API_KEY)['metadata']['participants']
print(len(praticipants))

for puuid in praticipants:
    gameName, tagLine = get_gameName_and_tagLine_from_puuid(puuid, PLATFORM, API_KEY)
    print(f"{gameName}#{tagLine}")

def get_gameStartTimestamp(match_id, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("gameStartTimestamp")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None
    
start_time = datetime.fromtimestamp(get_gameStartTimestamp(match_history[0], PLATFORM, API_KEY)/1000)
print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")


def get_gameEndTimestamp(match_id, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("gameEndTimestamp")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None
    
end_time = datetime.fromtimestamp(get_gameEndTimestamp(match_history[0], PLATFORM, API_KEY)/1000)
print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")


def get_endOfGameResult(match_id, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("endOfGameResult")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None

print(get_endOfGameResult(match_history[0], PLATFORM, API_KEY))

def get_gameDuration(match_id, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("gameDuration")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None

def get_gameCreation(match_id, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("gameCreation")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None


# sposob liczenia daty meczu dla op.gg
print(datetime.fromtimestamp(get_gameCreation(match_history[1], PLATFORM, API_KEY)/1000) + timedelta(seconds=get_gameDuration(match_history[1], PLATFORM, API_KEY)))

print(len(get_match_history(get_puuid(gameName, tagLine, PLATFORM, API_KEY), PLATFORM, API_KEY)))