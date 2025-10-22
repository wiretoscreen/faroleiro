import modules.bulkdeleter
import modules.bulkleaver
import modules.bulkunrelationship
import argparse, json, os

cfg_path = "config.json"
default_cfg = {"token": "YourDiscordAccountToken", "ignore": ["Array", "of", "guilds", "to", "ignore", "on", "guilds", "cleaner"], "friendsignore": ["FriendIds to Ignore"]}

parser = argparse.ArgumentParser()
parser.add_argument("--clear-messages", action="store_true", help="include message cleaning")
parser.add_argument("--leave-guilds", action="store_true", help="include guilds cleaning")
parser.add_argument("--remove-friends", action="store_true", help="include guilds cleaning")

args = parser.parse_args()

def checkArguments():
    if not any(vars(args).values()):
        print(f"use python {os.path.basename(__file__)} --help for instructions")
        exit()
    
    if args.clear_messages:
        cid = input("Channel ID to be cleared: ")
        content = input("Content to be deleted (leave empty for all messages): ")
        uid = input("Your account User ID: ")
        modules.bulkdeleter.run(
            token = cfg["token"],
            content = content,
            user_id = uid,
            channel_id = cid
        )
    
    if args.leave_guilds:
        modules.bulkleaver.run(
            token = cfg["token"],
            ignores = cfg["ignore"]
        )
    
    if args.remove_friends:
        modules.bulkunrelationship.run(
            token = cfg["token"],
            ignores = cfg["friendsignore"]
        )
        
def checkConfig():
    global cfg
    if not os.path.exists(cfg_path):
        json.dump(default_cfg, open(cfg_path, "w"), indent=4)
        exit(print("config.json was created, configure before running."))
    
    try:
        cfg = json.load(open(cfg_path))
    except json.JSONDecodeError:
        exit(print("ERROR: config.json poorly formatted, script can't run."))
        
checkConfig()
checkArguments()