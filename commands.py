import discord
from discord.ext import commands

from utils import load_csv_to_dict, update_dict_to_csv
from config import admin_id

file_path = "data/members.csv"
users_data = load_csv_to_dict(file_path)

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Enable the message content intent
intents.messages = True
intents.reactions = True

# Define the bot command prefix and intents
bot = commands.Bot(command_prefix='tv ', intents=intents)

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

react_messages = set()
roles_emojis = {
    'Role1': '🟢',  
    'Role2': '🔵',
    'Role3': '🔴',
}
# This function sets up the role channel where the bot sends a message, 
# and all needed emoji reactions
@bot.command(name='createrole')
async def send_role_messages(ctx):
    channel = bot.get_channel(1265349169317413027)
    if channel is None:
        print(f'Channel with ID 1265349169317413027 not found.')
        return

    for role, emoji in roles_emojis.items():
        message = await channel.send(f'React with {emoji} to get the {role} role!')
        await message.add_reaction(emoji)
        react_messages.add(message.id)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.id not in react_messages:
        return

    guild = reaction.message.guild
    role = discord.utils.get(guild.roles, name="new role")  # Role to be assigned
    if role:
        await user.add_roles(role)
        await reaction.message.channel.send(f'{user.mention} has been given the {role.name} role.')

@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return

    if reaction.message.id not in react_messages:
        return

    guild = reaction.message.guild
    role = discord.utils.get(guild.roles, name="new role")  # Role to be removed
    if role:
        await user.remove_roles(role)
        await reaction.message.channel.send(f'{user.mention} has been removed from the {role.name} role.')
