import requests 

def getUserID(token):
    return requests.get("https://discord.com/api/v9/users/@me", headers={"authorization": token, "User-Agent": "Discord-Android/126021"}).json()["id"]
