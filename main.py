"""
"""
import poker_scrape
import poker_save
import os
import discord
from discord.ext import commands
import game

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents = intents, command_prefix='!')

id_query = ''


@client.event
async def on_ready():
	"""
	Performs logic when the bot is 'Ready'.
	"""
	print('Poker Bot Ready!')


@client.command()
async def test(ctx):
	"""
	
	"""
	poll_members(ctx, ['biden', 'manchin'])



@client.command()
async def track(ctx, *, url):
	"""
	Tracks a PokerNow URL.

	Parameter url: The PokerNow URL that represents the Game to track.
	Precondition: url is a string and a valid PokerNow URL.

	Creates a new Game object and immediately updates all nets and people.
	"""
	pass


@client.command()
async def assign(ctx, *, member : discord.Member = None):
	"""
	Assigns `id_query` to `member`. 
	"""

	if id_query == '': #Someone types !assign but PokerBot isn't polling
		await ctx.send("I am not currently matching PokerNow IDs with Discord members.")
		return


async def poll_members(ctx, new_ids):
	"""
	For every PokerNow ID in `new_ids`, polls for a Discord ID.

	For example, if new_ids = ['a','b','c'], then PokerBot asks:
		"New PokerNow ID found: who is 'a'? Type !assign [discord_name] if it's you."
		...
		"New PokerNow ID found: who is 'b'? Type !assign [discord_name] if it's you."
		...
		"New PokerNow ID found: who is 'c'? Type !assign [discord_name] if it's you."

	A !assign is only valid if the [discord_name.id] matches the [author.id].
	"""
	for poker_id in new_ids:
		await ctx.send("New PokerNow ID found: **" + poker_id + "**. Type !assign [person].")
		id_query = poker_id
		while id_query != '':
			pass


if __name__ == '__main__':
	# """
	# """
	# url = 'https://www.pokernow.club/games/pglfGWYiDhD618K4dly9jFOh_'

	# #THIS IS TO GO IN "TRACK"

	# #1. Scrape data.
	# scraped_data = poker_scrape.scrape_ledger_data(url)
	
	# #2. Update everyone's net balances.
	# poker_save.update_all_balances(scraped_data)

	# #3. Get new/foreign PokerNow IDs in the updated NET file.
	# new_ids = poker_save.get_foreign_ids()

	# #4. Poll users to match new Poker IDs to Discord IDs.
	# pass
	client.run(os.getenv('TOKEN'))