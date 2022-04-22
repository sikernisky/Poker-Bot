"""
"""
import poker_scrape
import poker_save
import os
import discord
from discord.ext import commands
import game
from dotenv import load_dotenv
from discord.ext import tasks
import pymongo


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents = intents, command_prefix='!')
cluster = pymongo.MongoClient(os.getenv('MONGO'))



@client.event
async def on_ready():
	"""
	Prints a message to the console to confirm that Poker Bot is ready.

	The message is 'Poker Bot Ready!'
	"""
	print('Poker Bot Ready!')
	game.PokerGame.cluster = cluster



@client.command()
async def stats(ctx):
	"""
	Scrapes the current PokerNow game to send accumulated net balances along
	with the live net balances.

	If there is no active PokerNow game, sends accumulated net balances.
	"""
	await ctx.send("Please give me a moment while I scrape live PokerNow data. . .")
	game.PokerGame.update_ctx = ctx
	nets = await game.PokerGame.current_game.live_nets()
	if nets is None:
		return
	else:
		computed = poker_save.compute_stats(nets, poker_save.previous_people())
		await game.print_poker_stats(ctx, client, computed)



@client.command()
async def wipe(ctx, * password):
	"""
	Wipes all data on this server.
	"""
	#return #Not allowing wipes right now.
	game.PokerGame.update_ctx = ctx
	db = cluster[str(ctx.message.guild.id)]
	stats_collection = db['stats']
	people_collection = db['people']
	stats_collection.drop()
	people_collection.drop()


	await ctx.send("Wiped files.")


@client.command()
async def track(ctx, *, url):
	"""
	Tracks a PokerNow URL.

	Creates a new PokerGame object and sets it to be the current game.
	"""

	await ctx.send("Tracking URL: **" + url + "**.")

	if game.PokerGame.current_game != None:
		await game.PokerGame.current_game.immortalize()

	game.PokerGame.update_ctx = ctx

	db = cluster[str(ctx.message.guild.id)]
	game.PokerGame.stats_collection = db['stats']
	game.PokerGame.people_collection = db['people']

	player_discord_ids = []
	prev_players = poker_save.previous_people()
	for k in prev_players:
		if isinstance(prev_players[k], str):
			player_discord_ids.append(prev_players[k])

	tracked_game = game.PokerGame(player_discord_ids, url)
	game.PokerGame.current_game = tracked_game



@client.command()
async def assign(ctx, *, member : discord.Member = None):
	"""
	Assigns `id_query` to `member`. 
	"""
	game.PokerGame.update_ctx = ctx
	if game.PokerGame.id_query == '': #Someone types !assign but PokerBot isn't polling
		await ctx.send("I am not currently matching PokerNow IDs with Discord members.")
		return

	if member == None:
		await ctx.send("That member does not exist in this server. Please try again.")

	poker_save.add_player(game.PokerGame.id_query, str(member.id))

	await ctx.send("I assigned the PokerNow ID: **" + game.PokerGame.id_query + "** to " + member.name  + ".")
	game.PokerGame.id_query = ''
	await game.PokerGame.current_game.poll_members(ctx)


client.run(os.getenv('TOKEN'))