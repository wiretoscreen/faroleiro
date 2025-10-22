import requests
import time
import os
from colorama import Fore, init

init(autoreset=True)

def get_guilds(token):
    return [g['id'] for g in requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"authorization": token,         "User-Agent": "Discord-Android/126021"}).json()]

def leave_all(token, ignores):
    headers = {
        "User-Agent": "Discord-Android/126021",
        "authorization": token
    }

    for gid in get_guilds(token):
        while True:
            if gid in ignores:
                break
                
            res = requests.delete(
                f"https://discord.com/api/v9/users/@me/guilds/{gid}",
                headers=headers
            )

            if res.status_code == 204:
                print(f"{Fore.RED}[LEAVE] {Fore.YELLOW}{gid}{Fore.RESET}")
                break
            
            if res.status_code == 400:
                print(f"{Fore.RED}[ERROR] {Fore.YELLOW}{gid}{Fore.RESET} - You probably have ownership of the Server")
                break

            elif res.status_code == 429:
                retry_after = res.json().get("retry_after", 1)
                print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {retry_after} seconds...")
                time.sleep(float(retry_after))
            else:
                print(f"{Fore.RED}[FAILED]{Fore.RESET} {res.status_code}: {res.text}")
                break


def run(token, ignores):
    """Executes the guild search and cleaning"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.LIGHTBLUE_EX}FAROLEIRO ====================> {Fore.RESET}")
    print("Leaving all Servers")
    leave_all(token, ignores)
    print(f"{Fore.GREEN}Finished.{Fore.RESET}")