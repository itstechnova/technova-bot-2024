import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Enable the message content intent

# Define the bot command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

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
        await ctx.send(f'Please enter the email you used to apply for TechNova')

    if email in users_data and not users_data[email]['Verified']:
        users_data[email]['Verified'] = True
        # !!! add verified role
        await ctx.send(f'Hello, {ctx.author.name}! Your verification is successful.')
    elif email in users_data and users_data[email]['Verified']:
        await ctx.send(f'Oops, someone has already verified using this email.')

# Run the bot
bot.run(TOKEN)
