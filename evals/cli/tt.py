import requests

resp = requests.post("http://172.16.33.2:8080/bloom", json={
        "input":"张明有120元钱，买书用去80%，买文具的钱是买书的15%．买文具用去多少元？",
    })

print(resp.json())
