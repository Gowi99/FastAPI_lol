# from fastapi import FastAPI, HTTPException
# import httpx


# API_KEY = "RGAPI-395a53c4-a766-4a96-b62c-0deff6330dbf"
# PLATFORM = "EUROPE" 
# REGION = "EUN1"
# gameName = "Gowi"
# tagLine = "420"

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello from FastAPI!"}

# @app.get("/summoner/{nickname}")
# def get_summoner(nickname: str):
#     url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nickname}"
#     headers = {"X-Riot-Token": API_KEY}

#     try:
#         response = httpx.get(url, headers=headers)
#         response.raise_for_status()
#         return response.json()
#     except httpx.HTTPStatusError as e:
#         # Zwraca dokładny kod błędu i treść z Riot API
#         raise HTTPException(
#             status_code=e.response.status_code,
#             detail={
#                 "riot_status_code": e.response.status_code,
#                 "riot_message": e.response.text
#             }
#         )

# ============================
from config import API_KEY
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import httpx
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# PLATFORM = "EUROPE" 
# REGION = "EUN1"

def get_puuid(gameName, tagLine, PLATFORM, API_KEY):
    # Walidacja platformy
    valid = {"EUROPE", "AMERICAS", "ASIA", "SEA"}
    if PLATFORM not in valid:
        raise HTTPException(status_code=400, detail=f"Nieprawidłowa platforma: {PLATFORM}")
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200: 
        return response.json().get("puuid")
    else:
        return f"Error: {response.status_code}, {response.text}"

# def get_puuid(gameName, tagLine, PLATFORM, API_KEY):
#     # Walidacja platformy
#     valid = {"EUROPE", "AMERICAS", "ASIA", "SEA"}
#     if PLATFORM not in valid:
#         raise HTTPException(status_code=400, detail=f"Nieprawidłowa platforma: {PLATFORM}")

    url = f"https://{PLATFORM.lower()}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    # print("DEBUG URL:", url)  # odkomentuj na chwilę
    resp = httpx.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json().get("puuid")

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
    return templates.TemplateResponse("form.html", {"request": request})

# Obsługa formularza
# @app.post("/get-puuid", response_class=HTMLResponse)
# async def get_puuid_route(request: Request, gameName: str = Form(...), tagLine: str = Form(...), region: str = Form(...)):
#     platform = region_to_platform(region)
#     puuid = get_puuid(gameName, tagLine, platform, API_KEY)
#     return templates.TemplateResponse("result.html", {"request": request, "puuid": puuid})

@app.post("/get-puuid", response_class=HTMLResponse) # Wypierdala błąd 500, chyba problem z selectem w form.html
async def get_puuid_route(request: Request, gameName: str = Form(...), tagLine: str = Form(...), region: str = Form(...)):
    platform = region_to_platform(region)
    if not platform:
        raise HTTPException(status_code=400, detail=f"Nieznany region: {region}")
    puuid = get_puuid(gameName, tagLine, platform, API_KEY)
    return templates.TemplateResponse("result.html", {"request": request, "puuid": puuid})


@app.post("/test", response_class=HTMLResponse)
async def test(request: Request, gameName: str = Form(...), tagLine: str = Form(...), region: str = Form(...)):
    return templates.TemplateResponse("test.html", {"request": request, "gameName": gameName, "tagLine": tagLine, "region": region})
