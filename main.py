from fastapi import FastAPI, HTTPException
import httpx


API_KEY = "RGAPI-0cc0880e-d04d-4ee8-83cb-a085234aa079" 
REGION = "eun1"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/summoner/{nickname}")
def get_summoner(nickname: str):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nickname}"
    headers = {"X-Riot-Token": API_KEY}

    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        # Zwraca dokładny kod błędu i treść z Riot API
        raise HTTPException(
            status_code=e.response.status_code,
            detail={
                "riot_status_code": e.response.status_code,
                "riot_message": e.response.text
            }
        )
