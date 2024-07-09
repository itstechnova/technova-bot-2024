# Installation
Create a virtual environment by running:
```bash
python -m venv venv
```

Activate the virtual environment:

On Windows:
```bash
venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

After creating and activating your virtual environment, you can install the requirements from the requirements.txt file by running:

```bash
pip install -r requirements.txt
```

Copy the env.sample file to .env and add your Discord bot token. 

To run the bot, 
```bash
python bot.py
```
You will notice on the sample Technova server, the bot will show as online. Feel free to test commands now (e.g. !hello)

# Troubleshooting
If the bot seems to hang or doesn't start correctly, ensure that the bot isn't already running or online from a previous session.
