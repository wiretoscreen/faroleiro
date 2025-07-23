import requests
import time
import os
from colorama import *

print(f"{Fore.LIGHTBLUE_EX}FAROLEIRO ====================> {Fore.RESET}")
TOKEN = input("What's your Token? >> ")
ID = input("What's your User ID? >> ")
CHANNEL = input("Channel ID? >> ")
CONTENT = input("Content to Search & Delete (Leave blank for All Messages) >> ")

headers = {
    "User-Agent": "Discord-Android/126021",
    "authorization": TOKEN
}

def getMessages(channelId, authorId, content):
    all_messages = []
    offset = 0
    while True:
        res = requests.get(f"https://discord.com/api/v9/channels/{channelId}/messages/search?content={content}&author_id={authorId}&offset={offset}", headers=headers)
        if res.status_code == 429:
            retry_after = res.json().get("retry_after", 1)
            print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {retry_after} seconds...")
            time.sleep(float(retry_after))
            continue
        if not res.ok:
            break
        res = res.json()
        all_messages += res["messages"]
        offset += 25
        if offset >= res["total_results"]:
            break
        time.sleep(1)
    return { "messages": all_messages }
    
def deleteMessages(channelId, messages):
    for _ in messages["messages"]:
        while True:
            res = requests.delete(f"https://discord.com/api/v9/channels/{channelId}/messages/{_[0]['id']}", headers=headers)         
            if res.status_code == 204:
                print(f"{Fore.RED}[DELETED] {Fore.YELLOW}{_[0]['id']}{Fore.RESET}: {_[0]['content']}")
                break
            elif res.status_code == 429:
                retry_after = res.json().get("retry_after", 1)
                print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {retry_after} seconds...")
                time.sleep(float(retry_after))
            else:
                break

    
def start():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.LIGHTBLUE_EX}FAROLEIRO ====================> {Fore.RESET}")
    print("Fetching Messages... (This will probably take a while.)")
    messages = getMessages(CHANNEL, ID, CONTENT)
    time.sleep(10)
    print("Deleting Messages...")
    deleteMessages(CHANNEL, messages)
    
    
start()