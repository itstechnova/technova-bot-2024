import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import csv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Enable the message content intent

# Admin
admin_id = '780915204204134410'

# Define the bot command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

def load_csv_to_dict(file_path):
    df = pd.read_csv(file_path)
    data_dict = df.set_index("Email").to_dict(orient="index")
    return data_dict

def update_dict_to_csv(file_path, data_dict):
    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    # Write DataFrame to CSV
    df.to_csv(file_path, index_label='Email')

file_path = "members.csv"
users_data = load_csv_to_dict(file_path)
print(users_data)

# List to hold event data
events = []

# Load events from CSV
def load_events():
    global events
    with open('events.csv', newline='') as csvfile:
        event_reader = csv.DictReader(csvfile)
        events = [
            {
                'event_name': row['event_name'],
                'event_time': datetime.strptime(row['event_time'], '%Y-%m-%d %H:%M:%S'),
                'message': row['message']
            }
            for row in event_reader
        ]
    # Add a test event that runs immediately for testing
    test_event = {
        'event_name': 'Immediate Test Event',
        'event_time': datetime.now(),
        'message': 'This is a test event message that runs immediately.'
    }
    events.append(test_event)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    load_events()
    check_events.start()

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

# Example command
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# Verify command
@bot.command(name='verify')
async def verify(ctx, email):
    if not email or email not in users_data:
        print(email)
        print(users_data)
        await ctx.send(f'Please enter the email you used to apply for TechNova')

    if email in users_data and not users_data[email]['Verified']:
        users_data[email]['Verified'] = True
        update_dict_to_csv(file_path, users_data)

        # Add verified role
        try:
            user_id = ctx.author.id
            guild_id = ctx.guild.id

            guild = bot.get_guild(guild_id)
            if guild is None:
                await ctx.send(f"Guild with ID {guild_id} not found.")
                return

            member = guild.get_member(user_id)
            if member is None:
                await ctx.send(f"Member with ID {user_id} not found.")
                return

            role = discord.utils.get(guild.roles, name="Verified")
            if role is None:
                await ctx.send("Role 'Verified' not found.")
                return

            await member.add_roles(role)
        except Exception as e:
            await ctx.send(f"Failed to add role: {e}")
            dm_admin(ctx, f"Failed to add role: {e}")

        await ctx.send(f'Hello, {ctx.author.name}! Your verification is successful.')
    elif email in users_data and users_data[email]['Verified']:
        await ctx.send(f'Oops, someone has already verified using this email.')
        await dm_admin(ctx, f'Oops, someone has already verified using this email: {email}')

async def dm_admin(ctx, message):
    try:
        user = await bot.fetch_user(admin_id)
        await user.send(message)
        print(f"Message sent to {user.name}")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Task to check events and send announcements
@tasks.loop(seconds=60)  # Check every minute
async def check_events():
    now = datetime.now()
    for event in events:
        if now >= event['event_time']:
            channel = bot.get_channel(1265349169317413027)
            if channel:
                await channel.send(event['message'])
            events.remove(event)  # Remove event after announcement

# Run the bot
bot.run(TOKEN)
