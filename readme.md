> ⚠️ Migrated to Codeberg (Github is a Mirror)

# Faroleiro

<div align="center">
<a href="https://python.org" target="_blank"><img src="https://badgen.net/badge/Made with/Python/blue?icon"></a>
<a href="https://www.gnu.org/licenses/gpl-3.0.html" target="_blank"><img src="https://badgen.net/badge/Free Software/GPLv3.0+/black?icon"></a>
</div>

<div align="center">
<p>Faroleiro is a CLI Tool to clear Discord Accounts</p>
<p>Stay safe when trading or selling accounts or deleting personal information from Discord.</p>
</div>

---

## ✶ Installation (from GitHub Releases)

1. Open the repository Releases page (e.g. `https://github.com/wiretoscreen/Faroleiro/releases`) and download the latest release archive (`.zip` or `.tar.gz`).

2. Extract the downloaded archive:
   ```bash
   unzip Faroleiro-X.Y.Z.zip
   cd Faroleiro-X.Y.Z
   ```

3. Make sure you have Python 3.8+ installed:
   ```bash
   python3 --version
   ```

4. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

5. Configure `config.json` (see **Configuration** below)

---

## ✸ Configuration

When run for the first time the script will create a `config.json` with default values. Default example created by the script:

```json
{
  "token": "YourDiscordAccountToken",
  "ignore": ["Array", "of", "guilds", "to", "ignore", "on", "guilds", "cleaner"],
  "friendsignore": ["FriendIds to Ignore"],
  "dmsignore": ["DMIds to Ignore"],
  "connectionsignore": ["connections types do ignore (consult readme.md for types)"]
}
```

**Edit `config.json` before running** and set:
- `token`: your Discord account token (dangerous to share — see warnings).
- `ignore`: list of guild IDs to skip when leaving guilds.
- `friendsignore`: list of friend IDs to skip when removing friends.
- `dmsignore`: list of DM IDs to skip when closing DMs.
- `connectionsignore`: list of connection IDs to skip when clearing connections.
---

## ✹ Usage

`main.py` exposes several CLI flags. Examples below assume you're in the project folder and using `python3`:

Show help:
```bash
python3 main.py --help
```

Available flags:
- `--login` — starts qrcode login flow, sometimes returns captcha. Let's go gambling.
- `--clear-messages` — run message clearing, subflags:
  - `--cm-content` — content to search & delete (do not include if you are going to delete everything)
  - `--cm-channel` — channel id
- `--leave-guilds` — leave all guilds except those listed in `ignore`
- `--remove-friends` — remove friends (except those in `friendsignore`)
- `--close-dms` — close DMs (except those in `dmsignore`)
- `--clear-connections` — remove Connections (except those in `connectionsignore`)

Example: leave guilds and remove friends:
```bash
python3 main.py --leave-guilds --remove-friends
```

Example: clear messages from a specific channel:
```bash
python3 main.py --clear-messages --cm-channel 012345678910
```

Example: clear messages from a specific channel with specific content:
```bash
python3 main.py --clear-messages --cm-channel 012345678910 --cm-content "foo"
```

---

## ✶ Connections IDs

> INFO: Use the ids in the clear connections function ignore list

| ID                | Display Name                    |
|--------------------|----------------------------------|
| amazon-music       | Amazon Music                     |
| battlenet          | Battle.net                       |
| bluesky            | Bluesky                          |
| bungie             | Bungie.net                        |
| contacts           | Contact Sync                     |
| crunchyroll        | Crunchyroll                      |
| domain             | Domain                           |
| ebay               | eBay                             |
| epicgames          | Epic Games                       |
| facebook           | Facebook                         |
| github             | GitHub                           |
| instagram          | Instagram                        |
| leagueoflegends    | League of Legends                |
| mastodon           | Mastodon                         |
| paypal             | PayPal                           |
| playstation        | PlayStation Network              |
| playstation-stg    | PlayStation Network (Staging)    |
| reddit             | Reddit                           |
| roblox             | Roblox                           |
| riotgames          | Riot Games                       |
| samsung            | Samsung Galaxy                   |
| soundcloud         | SoundCloud                       |
| spotify            | Spotify                          |
| skype              | Skype                            |
| steam              | Steam                            |
| tiktok             | TikTok                           |
| twitch             | Twitch                           |
| twitter            | Twitter                          |
| xbox               | Xbox                             |
| youtube            | YouTube                          |
