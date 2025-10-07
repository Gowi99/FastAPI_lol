# gracz1igracz2.namesitags -> puuids
# puuids == puuid1 i puuid2
# puuid1i2 -> pobierz historie -> if mecz_z_h1 in historia2 -true-> wspolny
#                              -> if gracz1 i gracz2 in mecz_z_h1

# mozna zrobic wykres winratio na przestrzeni np. tygodnia, miesiaca, roku
# mozna zrobic wybor z listy bohaterow a pozniej winratio dzienne z tygodnia
import logging
from pydantic import BaseModel
from config import API_KEY
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# PLATFORM = "EUROPE" 
# REGION = "EUN1"

def get_puuid(gameName, tagLine, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200: 
        return response.json().get("puuid")
    elif response.status_code == 403:
        logging.error("API key")
        return "Error: API key."
    elif response.status_code == 401:
        logging.error("API key.")
        return "Error: API key."
    else:
        return f"Error: {response.status_code}, {response.text}"


def get_last_100_matches_by_puuid(puuid: str, PLATFORM: str, API_KEY: str) -> list:
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=100"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


# sprawdzic zwyciestwo dla kazdego meczu i zwrocic %
def winrate(list_of_matches):   
    pass


# jedyne zagrożenie to zagranie tego samego meczu w przeciwnych drużynach 
# (liczy jako wspolny mecz, mozna wykluczyc sprawdzajac czy puuid1 i puuid2 sa w participants albo winratio dla kazdego)
def last_10_common_matches_winrate(puuid1: str, puuid2: str, PLATFORM: str, API_KEY: str) -> list:
    match_history1 = get_last_100_matches_by_puuid(puuid1, PLATFORM, API_KEY)
    match_history2 = get_last_100_matches_by_puuid(puuid2, PLATFORM, API_KEY)
    i = 0
    common_matches = []
    for match in match_history1:
        if match in match_history2:
            common_matches.append(match)
            i += 1
        if i == 10:
            return common_matches[:10]
    return common_matches       
    

def region_to_platform(region: str) -> str:
    mapping = {
        "eune": "EUROPE",
        "euw": "EUROPE",
        "na": "AMERICAS",
        "lan": "AMERICAS",
        "las": "AMERICAS",
        "br": "AMERICAS",
        "kr": "ASIA",
        "jp": "ASIA",
        "oce": "SEA",
        "tr": "EUROPE",
        "ru": "EUROPE",
    }
    return mapping.get(region.lower(), "EUROPE")


# Strona z formularzem
@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form_2_players.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def get_puuid_route(request: Request, gameName1: str = Form(...), tagLine1: str = Form(...), region1: str = Form(...), gameName2: str = Form(...), tagLine2: str = Form(...), region2: str = Form(...)):
    platform1 = region_to_platform(region1)
    platform2 = region_to_platform(region2)
    if not platform1:
        raise HTTPException(status_code=400, detail=f"Nieznany region: {region}")
    if not platform2:
        raise HTTPException(status_code=400, detail=f"Nieznany region: {region}")
    puuid1 = get_puuid(gameName1, tagLine1, platform1, API_KEY)
    puuid2 = get_puuid(gameName2, tagLine2, platform2, API_KEY)
    winrate = None  # Tu bedzie trzeba dorzucic winrate
    if puuid1.startswith("Error") or puuid2.startswith("Error"):
        return templates.TemplateResponse("form_2_players.html", {"request": request, "error": f"Błędne dane", "puuid1": puuid1, "puuid2": puuid2})
    return templates.TemplateResponse("result.html", {"request": request, "gameName1": gameName1,"tagLine1": tagLine1, "gameName2": gameName2,"tagLine2": tagLine2, "puuid1": puuid1, "puuid2": puuid2, "winrate": winrate})

# @app.get("/last10gameswinrate", response_class=HTMLResponse)
# async def last10gameswinrate(request: Request):
#     return templates.TemplateResponse("result.html", {"request": request})  # Tu bedzie trzeba dorzucic winrate

@app.post("/test", response_class=HTMLResponse)
async def test(request: Request, gameName: str = Form(...), tagLine: str = Form(...), region: str = Form(...)):
    return templates.TemplateResponse("test.html", {"request": request, "gameName": gameName, "tagLine": tagLine, "region": region})

