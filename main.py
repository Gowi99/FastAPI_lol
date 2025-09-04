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

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import httpx
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "RGAPI-395a53c4-a766-4a96-b62c-0deff6330dbf"
PLATFORM = "EUROPE" 
REGION = "EUN1"

def get_puuid(gameName, tagLine, PLATFORM, API_KEY):
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200: 
        return response.json().get("puuid")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Strona z formularzem
@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Obsługa formularza
@app.post("/get-puuid", response_class=HTMLResponse)
async def get_puuid_route(request: Request, gameName: str = Form(...), tagLine: str = Form(...), platform: str = Form(...)):
    puuid = get_puuid(gameName, tagLine, platform, API_KEY)
    return templates.TemplateResponse("result.html", {"request": request, "puuid": puuid})
