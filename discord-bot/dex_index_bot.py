import discord
import requests
import json
from discord.ext import commands, tasks

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
GITHUB_REPO = "DexIndex0/DexIndex0"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@tasks.loop(minutes=10)
async def check_repo_updates():
    # Fetch the latest commits
    response = requests.get(f"{GITHUB_API_URL}/commits")
    if response.status_code == 200:
        commits = response.json()
        latest_commit = commits[0]['commit']['message']
        channel = bot.get_channel(YOUR_CHANNEL_ID)  # replace with your channel ID
        await channel.send(f"New commit in {GITHUB_REPO}: {latest_commit}")

@bot.command()
async def pokedex(ctx, *, pokemon_name: str):
    # Fetch Pokémon data from an API (replace with actual API URL)
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if response.status_code == 200:
        data = response.json()
        await ctx.send(f"{data['name'].capitalize()} - Height: {data['height']}, Weight: {data['weight']}")
    else:
        await ctx.send("Pokémon not found!")

@bot.command()
async def issues(ctx):
    response = requests.get(f"{GITHUB_API_URL}/issues")
    if response.status_code == 200:
        issues = response.json()
        issue_list = "\n".join([f"Issue #{issue['number']}: {issue['title']}" for issue in issues])
        await ctx.send(f"Issues in {GITHUB_REPO}:\n{issue_list}")
    else:
        await ctx.send("Failed to fetch issues.")

@bot.command()
async def pr(ctx):
    response = requests.get(f"{GITHUB_API_URL}/pulls")
    if response.status_code == 200:
        prs = response.json()
        pr_list = "\n".join([f"PR #{pr['number']}: {pr['title']}" for pr in prs])
        await ctx.send(f"Open Pull Requests in {GITHUB_REPO}:\n{pr_list}")
    else:
        await ctx.send("Failed to fetch pull requests.")

check_repo_updates.start()

bot.run(TOKEN)