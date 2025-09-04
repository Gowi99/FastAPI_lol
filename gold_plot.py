import requests
import matplotlib.pyplot as plt

API_KEY = "TWÓJ_API_KEY"
MATCH_ID = "EUN1_1234567890"
REGION = "europe"

# 1. Pobierz dane timeline
url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{MATCH_ID}/timeline?api_key={API_KEY}"
response = requests.get(url)
timeline = response.json()

# 2. Przygotuj dane złota dla graczy
frames = timeline['info']['frames']

# Każdy gracz ma id od 1 do 10 (participantId)
gold_over_time = {pid: [] for pid in range(1, 11)}
timestamps = []

for frame in frames:
    timestamps.append(frame['timestamp'] // 60000)  # minuta gry
    for participant_id, pdata in frame['participantFrames'].items():
        gold_over_time[int(participant_id)].append(pdata['totalGold'])

# 3. Rysowanie wykresu (np. dla wszystkich graczy)
plt.figure(figsize=(12, 6))
for pid, gold in gold_over_time.items():
    plt.plot(timestamps, gold, label=f'Gracz {pid}')
    
plt.title('Gold w czasie dla każdego gracza')
plt.xlabel('Minuta gry')
plt.ylabel('Łączne złoto')
plt.legend()
plt.grid(True)
plt.show()