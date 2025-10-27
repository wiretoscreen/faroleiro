import requests
import time 
from colorama import Fore, init

init(autoreset=True)

headers = {
    "Authorization": token,
    "User-Agent": "Discord/126021 Android",
} 

def fetch_servers(token, headers):
    url = "https://discord.com/api/v10/users/@me/guilds"
    response = requests.get(url, headers=headers)
    servers = response.json()
    owned_servers = []
    for server in servers:
        if server["owner"] == True:
            server_id = server["id"]
            server_name = server["name"]
            owned_servers.append({
                "name": server_name,
                "id": server_id
            })
    if not owned_servers:
        print(f"{Fore.YELLOW}[INFO]{Fore.RESET} No servers available for deletion")
        return
    else:
        return owned_servers

def delete_servers(token, headers):
    url = "https://discord.com/api/v10/guilds/"
    servers = fetch_servers(token, headers)
    
    if not servers:
        return
        
        
    for server in servers:
        server_id = server["id"]
        server_name = server["name"]

        while True:
        
            req = requests.delete(url + server_id, headers=headers)

            if req.status_code == 429:
                rtf = req.json().get("retry_after", 5)
                print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {rtf} seconds....")
                time.sleep(rtf)
                continue

            try:
                status = req.json().get("code")
            except:
                status = None

            if req.status_code == 204 and status != 60003:
                print(f"{Fore.GREEN}[DELETED]{Fore.RESET} {server_name} ({server_id})")
                break
            elif status == 60003:
                print(f"{Fore.RED}[ERROR]{Fore.RESET} Disable MFA for this operation")
                return
            else:
            
                print(f"{Fore.RED}[FAILED]{Fore.RESET} {server_name} ({server_id}) - Error status {status}")
                break



def run(token):
"""Executes the delete servers"""
    print("removing all servers")
    delete_servers(token, headers)
    print("finished!")
