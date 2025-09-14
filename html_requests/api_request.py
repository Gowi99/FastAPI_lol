import httpx
from config import API_KEY


#  .venv/bin/python3 -m html_requests.api_request

def get_puuid():
    url = f"http://127.0.0.1:8000/"
    headers = {}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200: 
        return response
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def post_puuid(gameName, tagLine, region):
    url = f"http://127.0.0.1:8000/get-puuid"

    headers = {"Content-Type": "application/json"}

    payload = {"gameName": gameName,
                "tagLine": tagLine,
                "region": region}

    response = httpx.post(url, data=payload)
    if response.status_code == 200: 
        return response
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

puuid = post_puuid('Gowi', "420", "kr") # trzeba sprawdzić czy na pewno wykrywa, ze jest 'kr' a nie 'eune' 
print(puuid)
print(puuid.text)


# # print(get_puuid().text)
# print(post_puuid("Gowi", "420", "eune"))
# print(post_puuid("Gowi", "420", "").puuid)
# print(post_puuid("Gowi", "420", "euw").__dir__())