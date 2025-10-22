import requests
import time
import os
from colorama import Fore, init

init(autoreset=True)

def get_dms(token):
    return [g['id'] for g in requests.get("https://discord.com/api/v9/users/@me/channels", headers={"authorization": token,         "User-Agent": "Discord-Android/126021"}).json()]

def close_all(token, ignores):
    headers = {
        "User-Agent": "Discord-Android/126021",
        "authorization": token
    }

    for uid in get_dms(token):
        while True:
            if uid in ignores:
                break
                
            res = requests.delete(
                f"https://discord.com/api/v9/channels/{uid}",
                headers=headers
            )

            if res.status_code == 200:
                print(f"{Fore.RED}[REMOVED] {Fore.YELLOW}{uid}{Fore.RESET}")
                break

            elif res.status_code == 429:
                retry_after = res.json().get("retry_after", 1)
                print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {retry_after} seconds...")
                time.sleep(float(retry_after))
            else:
                print(f"{Fore.RED}[FAILED]{Fore.RESET} {res.status_code}: {res.text}")
                break


def run(token, ignores):
    """Executes the dm search and cleaning"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.LIGHTBLUE_EX}FAROLEIRO ====================> {Fore.RESET}")
    print("Removing all DMs")
    close_all(token, ignores)
    print(f"{Fore.GREEN}Finished.{Fore.RESET}")