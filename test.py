from config import API_KEY
import httpx
from datetime import datetime, timedelta
from pydantic import BaseModel
import json

PLATFORM = "EUROPE" 
REGION = "EUN1"
gameName = "Gowi"
tagLine = "420"

class TeamDto(BaseModel):
    teamId: int | None = None
    win: bool | None = None

class ParticipantDto(BaseModel):
    teamId : int | None = None

class MetadataDto(BaseModel):
    pass

class InfoDto(BaseModel):
    gameCreation: int | None = None
    gameDuration: int | None = None
    gameEndTimestamp: int | None = None
    gameId: int
    gameMode: str | None = None
    gameName: str | None = None
    gameType: str | None = None
    gameVersion: str | None = None
    mapId: int | None = None
    participants: list[ParticipantDto]
    platformId: str | None = None
    queueId: int | None = None
    teams: list[TeamDto] | None = None
    tournamentCode: str | None = None

class MatchDto(BaseModel):
    metadata: MetadataDto
    info: InfoDto


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
        match = MatchDto(**response.json())
        return match.info
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# def get_gameName_and_tagLine_from_puuid(puuid, PLATFORM, API_KEY):
#     url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
#     headers = {"X-Riot-Token": API_KEY}
#     response = httpx.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("gameName"), data.get("tagLine")
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None, None

# def get_gameStartTimestamp(match_id, PLATFORM, API_KEY):
#     url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
#     headers = {"X-Riot-Token": API_KEY}
#     response = httpx.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("info", {}).get("gameStartTimestamp")
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None, None
    
# def get_gameEndTimestamp(match_id, PLATFORM, API_KEY):
#     url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
#     headers = {"X-Riot-Token": API_KEY}
#     response = httpx.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("info", {}).get("gameEndTimestamp")
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None, None
    
# def get_endOfGameResult(match_id, PLATFORM, API_KEY):
#     url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
#     headers = {"X-Riot-Token": API_KEY}
#     response = httpx.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("info", {}).get("endOfGameResult", {})
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None, None

# def get_gameDuration(match_id, PLATFORM, API_KEY):
#     url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
#     headers = {"X-Riot-Token": API_KEY}
#     response = httpx.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("info", {}).get("gameDuration")
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None, None

# def get_gameCreation(match_id, PLATFORM, API_KEY):
#     url = f"https://{PLATFORM}.api.riotgames.com/lol/match/v5/matches/{match_id}"
#     headers = {"X-Riot-Token": API_KEY}
#     response = httpx.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("info", {}).get("gameCreation")
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None, None


puuid = get_puuid(gameName, tagLine, PLATFORM, API_KEY)
# print(f"PUUID: {puuid}")

match_history = get_match_history(get_puuid(gameName, tagLine, PLATFORM, API_KEY), PLATFORM, API_KEY)
# print(match_history)

x = get_match_details(match_history[0], PLATFORM, API_KEY)
print(x.participants)

# # Pobieranie zawodników z historii meczów

# praticipants = get_match_details(match_history[0], PLATFORM, API_KEY)['metadata']['participants']
# print(len(praticipants))

# for puuid in praticipants:
#     gameName, tagLine = get_gameName_and_tagLine_from_puuid(puuid, PLATFORM, API_KEY)
#     print(f"{gameName}#{tagLine}")

# start_time = datetime.fromtimestamp(get_gameStartTimestamp(match_history[0], PLATFORM, API_KEY)/1000)
# print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# print(get_endOfGameResult(match_history[0], PLATFORM, API_KEY))

# end_time = datetime.fromtimestamp(get_gameEndTimestamp(match_history[0], PLATFORM, API_KEY)/1000)
# print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

# # sposob liczenia daty meczu dla op.gg
# print(datetime.fromtimestamp(get_gameCreation(match_history[1], PLATFORM, API_KEY)/1000) + timedelta(seconds=get_gameDuration(match_history[1], PLATFORM, API_KEY)))

# print(len(get_match_history(get_puuid(gameName, tagLine, PLATFORM, API_KEY), PLATFORM, API_KEY)))