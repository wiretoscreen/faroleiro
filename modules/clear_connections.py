import requests
import time
import os
from colorama import Fore, init

init(autoreset=True)

def get_connections(token):
    res = requests.get("https://discord.com/api/v9/users/@me/connections",headers={"authorization": token,"User-Agent": "Discord-Android/126021"}).json()

    return [{"type": c["type"], "id": c["id"], "name": c["name"]} for c in res]

def remove_connections(token, ignores):
    headers = {
        "User-Agent": "Discord-Android/126021",
        "authorization": token
    }

    for connection in get_connections(token):
        while True:
            if connection["type"] in ignores:
                break
                
            res = requests.delete(
                f"https://discord.com/api/v9/users/@me/connections/{connection['type']}/{connection['id']}",
                headers=headers
            )

            if res.status_code == 204:
                print(f"{Fore.RED}[REMOVED] {Fore.YELLOW}{connection['type']}{Fore.RESET} {connection['name']}")
                break

            elif res.status_code == 429:
                retry_after = res.json().get("retry_after", 1)
                print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {retry_after} seconds...")
                time.sleep(float(retry_after))
            else:
                print(f"{Fore.RED}[FAILED]{Fore.RESET} {res.status_code}: {res.text}")
                break


def run(token, ignores):
    """Executes the connection search and cleaning"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.LIGHTBLUE_EX}FAROLEIRO ====================> {Fore.RESET}")
    print("Removing all Connections")
    remove_connections(token, ignores)
    print(f"{Fore.GREEN}Finished.{Fore.RESET}")