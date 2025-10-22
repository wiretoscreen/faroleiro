import modules.bulkdeleter
import modules.bulkleaver
import modules.bulkunrelationship
import modules.bulkdmcloser
import modules.utils
import argparse, json, os

cfg_path = "config.json"
default_cfg = {"token": "YourDiscordAccountToken", "ignore": ["Array", "of", "guilds", "to", "ignore", "on", "guilds", "cleaner"], "friendsignore": ["FriendIds to Ignore"], "dmsignore": ["DMIds to Ignore"]}

parser = argparse.ArgumentParser()
parser.add_argument("--clear-messages", action="store_true", help="include message cleaning") # Invokes Clear Messages Function
parser.add_argument("--leave-guilds", action="store_true", help="include guilds cleaning") # Invokes Guild Leave Function
parser.add_argument("--remove-friends", action="store_true", help="include friends cleaning") # Invokes Friends Remover Function
parser.add_argument("--close-dms", action="store_true", help="include dms cleaning") # Invokes DM Closer Function

parser.add_argument("--cm-content", type=str, help="message content to search on clear messages")
parser.add_argument("--cm-channel", type=str, help="channel id to clear messages")

args = parser.parse_args()

def checkArguments():
    if not any(vars(args).values()):
        print(f"use python {os.path.basename(__file__)} --help for instructions")
        exit()
    
    if args.clear_messages:
        if not args.cm_channel:
            exit(parser.error("--cm-channel is required when using --clear-messages"))

        content = args.cm_content or ""

        modules.bulkdeleter.run(
            token = cfg["token"],
            content = content,
            user_id = modules.utils.getUserID(cfg["token"]),
            channel_id = args.cm_channel
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
    
    if args.close_dms:
        modules.bulkdmcloser.run(
            token = cfg["token"],
            ignores = cfg["dmsignore"]
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