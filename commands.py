import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from config import pronoun_roles, academic_roles, combined_roles, roles_channelID, announcement_channelID
from utils import *

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Enable the message content intent
intents.messages = True
intents.reactions = True

# Define the bot command prefix and intents
bot = commands.Bot(command_prefix='tv ', intents=intents)

file_path = "members.csv"
users_data = load_csv_to_dict(file_path)
print(users_data)

@tasks.loop(seconds=60)
async def check_announcements():
    now = datetime.utcnow()
    for announcement in scheduled_announcements:
        title, description, announce_time = announcement
        if announce_time <= now:
            channel = bot.get_channel(announcement_channelID)
            if channel:
                await channel.send(f"**{title}**\n{description}")
                scheduled_announcements.remove(announcement)  # Remove after sending

# Helper function to check for role existence and create it if missing
async def get_or_create_role(guild, role_info):
    role = guild.get_role(role_info['role_id'])
    if role is None:
        role = await guild.create_role(name=role_info['name'], color=discord.Color.random())
        # You might want to store the new role ID in a persistent way if needed
        role_info['role_id'] = role.id
        print(f"Created missing role: {role.name} with ID {role.id}")
    return role

# Function to create embed and add reactions
async def create_embed_and_reactions(ctx, title, description, roles_dict, color):
    embed = discord.Embed(title=title, description=description, color=color)
    
    for emoji, role_info in roles_dict.items():
        embed.add_field(name=f"{emoji} {role_info['name']}", value=f"", inline=False)
    
    message = await ctx.send(embed=embed)
    
    # Add reactions to the message
    for emoji in roles_dict:
        await message.add_reaction(emoji)

async def dm_admin(ctx, message):
    try:
        user = await bot.fetch_user(admin_id)
        await user.send(message)
        print(f"Message sent to {user.name}")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Setup message for users to react to change roles
@bot.command(name='setup_roles')
@commands.has_permissions(administrator=True)
async def setup(ctx):
   # Pronouns
    await create_embed_and_reactions(
        ctx,
        title="Pronouns",
        description="Choose your preferred pronoun(s) below:",
        roles_dict=pronoun_roles,
        color=discord.Color.blue()
    )
    
    # Academic Levels
    await create_embed_and_reactions(
        ctx,
        title="Academic Level!",
        description="Select your academic level:",
        roles_dict=academic_roles,
        color=discord.Color.green()
    )

# Setup message for announcement events
@bot.command(name='setup_events')
@commands.has_permissions(administrator=True)
async def announcement(ctx):
    global scheduled_announcements
    scheduled_announcements = read_events_csv("./announcements.csv")
    await ctx.send("Announcements have been scheduled.")
    check_announcements.start()

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

# Event: On reaction add
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.channel.id != roles_channelID:
        return
    
    role_info = combined_roles.get(str(reaction.emoji))
    if role_info:
        role = await get_or_create_role(reaction.message.guild, role_info)
        await user.add_roles(role)
        await user.send(f"You have been given the {role.name} role!")

# Event: On reaction remove
@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id != roles_channelID:
        return
    
    role_info = combined_roles.get(str(reaction.emoji))
    if role_info:
        role = await get_or_create_role(reaction.message.guild, role_info)
        await user.remove_roles(role)
        await user.send(f"The {role.name} role has been removed from you.")

