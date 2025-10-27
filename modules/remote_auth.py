import requests
import websocket
import threading
import time
import json
import base64
import qrcode_terminal
import os

from colorama import Fore
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
heartbeat_interval = 41250
private_key = None
public_key = None
cipher = None

def generateKeyPair():
    global private_key, public_key, cipher
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)

def heartbeat(ws):
    while True:
        ws.send(json.dumps({"op": "heartbeat"}))
        time.sleep(heartbeat_interval / 1000)

def decrypt_payload(encrypted_payload):
    """Decrypt base64 using OAEP + SHA256 (pycryptodome)"""
    payload_bytes = base64.b64decode(encrypted_payload)
    decrypted = cipher.decrypt(payload_bytes)
    return decrypted

def on_open(ws):
    generateKeyPair()

def on_message(ws, message):
    m = json.loads(message)
    if m["op"] == "hello":
        spki = public_key.export_key(format="DER")
        pk_encoded = base64.b64encode(spki).decode("utf-8")
        ws.send(json.dumps({"op": "init", "encoded_public_key": pk_encoded}))

        # Start heartbeat
        threading.Thread(target=heartbeat, args=(ws,), daemon=True).start()
    
    elif m["op"] == "cancel":
        exit(print("Operation canceled by User"))
        
    elif m["op"] == "pending_remote_init":
        qrcode_terminal.draw(f"https://discord.com/ra/{m['fingerprint']}")
        print("Fingerprint: " + m["fingerprint"])

    elif m["op"] == "nonce_proof":
        encrypted_nonce = m["encrypted_nonce"]
        nonce = decrypt_payload(encrypted_nonce)

        digest = SHA256.new(nonce).digest()
        nonce_proof = base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")

        ws.send(json.dumps({"op": "nonce_proof", "proof": nonce_proof}))
    
    elif m["op"] == "pending_ticket":
        p = decrypt_payload(m["encrypted_user_payload"])
        print(f"\nIn your phone, choose to proceed login with {Fore.LIGHTBLUE_EX}{p.decode("utf-8").split(":")[-1]}{Fore.RESET}")
    
    elif m["op"] == "pending_login":
        res = requests.post("https://discord.com/api/v9/users/@me/remote-auth/login", json = {"ticket": m["ticket"]}).json()
        print(res)
        
        if res.status_code == 200:
            if res["captcha_key"]:
                exit(print("[-] Got CAPTCHA, Try later."))
                
            token = decrypt_payload(res["encrypted_token"])
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        
            cfg["token"] = token
        
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=4)
            
            exit(print("[+] Logged in Successfully"))


ws = websocket.WebSocketApp(
    "wss://remote-auth-gateway.discord.gg/?v=2",
    header={"Origin": "https://discord.com"},
    on_open=on_open,
    on_message=on_message
)

def run():
    ws.run_forever()