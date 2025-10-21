import requests
import time
import os
from colorama import Fore, init

init(autoreset=True)

def get_messages(channel_id, author_id, content, token):
    headers = {
        "User-Agent": "Discord-Android/126021",
        "authorization": token
    }

    all_messages = []
    offset = 0
    while True:
        res = requests.get(
            f"https://discord.com/api/v9/channels/{channel_id}/messages/search",
            params={"content": content, "author_id": author_id, "offset": offset},
            headers=headers
        )

        if res.status_code == 429:
            retry_after = res.json().get("retry_after", 1)
            print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {retry_after} seconds...")
            time.sleep(float(retry_after))
            continue

        if not res.ok:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} {res.status_code}: {res.text}")
            break

        res = res.json()
        all_messages += res.get("messages", [])
        offset += 25

        if offset >= res["total_results"]:
            break
        time.sleep(1)

    return {"messages": all_messages}


def delete_messages(channel_id, messages, token):
    headers = {
        "User-Agent": "Discord-Android/126021",
        "authorization": token
    }

    for msg_group in messages["messages"]:
        msg = msg_group[0]
        while True:
            res = requests.delete(
                f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg['id']}",
                headers=headers
            )

            if res.status_code == 204:
                print(f"{Fore.RED}[DELETED] {Fore.YELLOW}{msg['id']}{Fore.RESET}: {msg['content']}")
                break

            elif res.status_code == 429:
                retry_after = res.json().get("retry_after", 1)
                print(f"{Fore.MAGENTA}[RATE LIMITED]{Fore.RESET} Waiting {retry_after} seconds...")
                time.sleep(float(retry_after))
            else:
                print(f"{Fore.RED}[FAILED]{Fore.RESET} {res.status_code}: {res.text}")
                break


def run(token, user_id, channel_id, content=""):
    """Executes the message search and cleaning"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.LIGHTBLUE_EX}FAROLEIRO ====================> {Fore.RESET}")
    print("Fetching Messages... (This will probably take a while.)")

    messages = get_messages(channel_id, user_id, content, token)
    time.sleep(5)

    print("Deleting Messages...")
    delete_messages(channel_id, messages, token)
    print(f"{Fore.GREEN}Finished.{Fore.RESET}")