#### DISCORD BOT
# WS Track
## **Lets you give away roles after time period.**
## Originally designed to track White Star events in game Hades' Star

---
### Local preparations (Linux/Debian/Ubuntu)
```
sudo apt install -y python3-pip
```
Install modules (second should be allready installed):
```
pip install discord.py
pip install python-dotenv
```

### Install App settings [DEV](https://discord.com/developers/applications)

You must be developer, then add new application and copy TOKEN to **.env**.

1. OAuth2 -> URL Generator, check BOT and Manage Roles. Then copy URL and run it.
2. Bot -> Create New
3. Bot -> Privileged Gateway Intents, check Presence Intent, Server Members Intent and Message Content Intent.
4. Copy TOKEN
5. Deploy. Can use service like [Replit](https://replit.com) to host script.

### Create invite/install BOT link
App/OAuth2 -> URL Generator -> check BOT -> Permissions: Manage Roles, Send Messages.

### Use on DC
After add bot thru OAuth2 URL, enter server roles and move up and down to choose
which roles bot can give or remove. All roles below bot's role are manageable for bot.
Now you can add bot's role to channel of choice.