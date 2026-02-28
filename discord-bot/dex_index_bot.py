import discord
from discord.ext import commands
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Discord bot configuration
bot = commands.Bot(command_prefix='!')

# GitHub API configuration
github_api_url = 'https://api.github.com/'
repository_owner = 'DexIndex0'
repository_name = 'DexIndex0'

# PokéAPI URL for Pokémon data
pokeapi_url = 'https://pokeapi.co/api/v2/pokemon/'

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')

@bot.command(name='issues')
async def fetch_issues(ctx):
    try:
        response = requests.get(f'{github_api_url}repos/{repository_owner}/{repository_name}/issues')
        issues = response.json()
        if not issues:
            await ctx.send('No issues found.')
            return
        for issue in issues:
            await ctx.send(f'Issue #{issue['number']}: {issue['title']} - {issue['html_url']}')
    except Exception as e:
        logging.error(f'Error fetching issues: {e}')
        await ctx.send('An error occurred while fetching issues.')

@bot.command(name='prs')
async def fetch_prs(ctx):
    try:
        response = requests.get(f'{github_api_url}repos/{repository_owner}/{repository_name}/pulls')
        prs = response.json()
        if not prs:
            await ctx.send('No pull requests found.')
            return
        for pr in prs:
            await ctx.send(f'PR #{pr['number']}: {pr['title']} - {pr['html_url']}')
    except Exception as e:
        logging.error(f'Error fetching PRs: {e}')
        await ctx.send('An error occurred while fetching pull requests.')

@bot.command(name='pokedex')
async def poke_lookup(ctx, *, pokemon_name: str):
    try:
        response = requests.get(f'{pokeapi_url}{pokemon_name}')
        if response.status_code == 200:
            poke_data = response.json()
            await ctx.send(f'{poke_data['name'].capitalize()} - Height: {poke_data['height']}, Weight: {poke_data['weight']}')
        else:
            await ctx.send(f'Pokémon {pokemon_name} not found.')
    except Exception as e:
        logging.error(f'Error fetching Pokémon data: {e}')
        await ctx.send('An error occurred while fetching Pokémon data.')

@bot.command(name='stats')
async def repository_stats(ctx):
    try:
        response = requests.get(f'{github_api_url}repos/{repository_owner}/{repository_name}')
        stats = response.json()
        await ctx.send(f'Repository: {stats['name']}, Stars: {stats['stargazers_count']}, Forks: {stats['forks_count']}')
    except Exception as e:
        logging.error(f'Error fetching repository stats: {e}')
        await ctx.send('An error occurred while fetching repository statistics.')

@bot.event
async def on_guild_channel_create(channel):
    await channel.send('Channel created!')

@bot.event
async def on_guild_channel_delete(channel):
    await channel.send('Channel deleted!')

# Running the bot
bot.run('')
