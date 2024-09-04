import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

roles_channelID = 1265349169317413027
announcement_channelID = 1265349169317413027

pronoun_roles = {
    "🟦": {"role_id": None, "name": "He/Him"},
    "🟥": {"role_id": None, "name": "She/Her"},
    "🟪": {"role_id": None, "name": "They/Them"},
}

academic_roles = {
    "🎒": {"role_id": None, "name": "High School"},
    "🎓": {"role_id": None, "name": "Undergraduate"},
    "📚": {"role_id": None, "name": "Graduate/Masters/PhD"},
    "🎖️": {"role_id": None, "name": "Postgraduate"},
    "🧑‍💻": {"role_id": None, "name": "Independent Study"},
}

# Combined dictionary for easy role management in reaction events
combined_roles = {**pronoun_roles, **academic_roles}
