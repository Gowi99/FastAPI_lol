from pydantic import BaseModel
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
    url = f"https://{PLATFORM}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200: 
        return response.json().get("puuid")
    else:
        return f"Error: {response.status_code}, {response.text}"


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
