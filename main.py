"""
"""
import poker_scrape
import poker_save
import os
import discord
from discord.ext import commands
from game import PokerGame
from dotenv import load_dotenv #Delete once on Heroku


load_dotenv() #Delete once on Heroku
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents = intents, command_prefix='!')


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
	PokerGame.new_ids = ['biden', 'manchin']
	await poll_members(ctx)


@client.command()
async def stats(ctx):
	"""
	"""
	await ctx.send(poker_save.stats())


@client.command()
async def wipe(ctx):
	"""
	"""
	poker_save.wipe_files()
	await ctx.send("Wiped files.")



@client.command()
async def track(ctx, *, url):
	"""
	Tracks a PokerNow URL.

	Parameter url: The PokerNow URL that represents the Game to track.
	Precondition: url is a string and a valid PokerNow URL.

	Creates a new Game object and immediately updates all nets and people.
	"""
	if not poker_scrape.valid_url(url):
		await ctx.send("That URL does not link to an active PokerNow game.")
		return
	await ctx.send("Tracking URL: **" + url + "**.")

	player_discord_ids = []
	prev_players = poker_save.previous_people()
	for k in prev_players:
		player_discord_ids.append(prev_players[k])

	tracked_game = PokerGame(player_discord_ids, url)

	scraped_data = poker_scrape.scrape_ledger_data(url)
	poker_save.update_all_balances(scraped_data)
	PokerGame.new_ids = poker_save.foreign_poker_ids()
	await poll_members(ctx)

# 	# #1. Scrape data.
# 	# scraped_data = poker_scrape.scrape_ledger_data(url)
	
# 	# #2. Update everyone's net balances.
# 	# poker_save.update_all_balances(scraped_data)

# 	# #3. Get new/foreign PokerNow IDs in the updated NET file.
# 	# new_ids = poker_save.get_foreign_ids()

# 	# #4. Poll users to match new Poker IDs to Discord IDs.
# 	# pass


@client.command()
async def assign(ctx, *, member : discord.Member = None):
	"""
	Assigns `id_query` to `member`. 
	"""

	if PokerGame.id_query == '': #Someone types !assign but PokerBot isn't polling
		await ctx.send("I am not currently matching PokerNow IDs with Discord members.")
		return

	if member == None:
		await ctx.send("That member does not exist in this server. Please try again.")

	poker_save.add_player(PokerGame.id_query, str(member.id))

	await ctx.send("I assigned the PokerNow ID: **" + PokerGame.id_query + "** to " + member.name  + ".")
	PokerGame.id_query = ''
	await poll_members(ctx)



async def poll_members(ctx):
	"""
	For every PokerNow ID in PokerGame.`new_ids`, polls for a Discord ID.

	For example, if new_ids = ['a','b','c'], then PokerBot asks:
		"New PokerNow ID found: who is 'a'? Type !assign [discord_name] if it's you."
		...
		"New PokerNow ID found: who is 'b'? Type !assign [discord_name] if it's you."
		...
		"New PokerNow ID found: who is 'c'? Type !assign [discord_name] if it's you."

	A !assign is only valid if the [discord_name.id] matches the [author.id].
	"""
	if PokerGame.new_ids == []:
		return

	poker_id = PokerGame.new_ids[0]
	if len(PokerGame.new_ids) == 1:
		PokerGame.new_ids = []
	else:
		PokerGame.new_ids = PokerGame.new_ids[1:]

	await ctx.send("New PokerNow ID found: **" + poker_id + "**. Type !assign [person].")
	PokerGame.id_query = poker_id
		

		# def check(m):
		# 	"""
		# 	Returns: True if m is in the format:

		# 	'!claim [some discord user]'
		# 	"""
		# 	keyword = '!assign'
		# 	return (len(m.content) >= (len(keyword) + 2) and m.content[:len(keyword)] == keyword
		# 		and m.content[len(keyword)] == ' ')
		# response = await client.wait_for('message', check = check, timeout=20)
		# print(response.content)


# if __name__ == '__main__':
# 	# """
# 	# """
# 	# url = 'https://www.pokernow.club/games/pglfGWYiDhD618K4dly9jFOh_'

# 	# #THIS IS TO GO IN "TRACK"

# 	# #1. Scrape data.
# 	# scraped_data = poker_scrape.scrape_ledger_data(url)
	
# 	# #2. Update everyone's net balances.
# 	# poker_save.update_all_balances(scraped_data)

# 	# #3. Get new/foreign PokerNow IDs in the updated NET file.
# 	# new_ids = poker_save.get_foreign_ids()

# 	# #4. Poll users to match new Poker IDs to Discord IDs.
# 	# pass

client.run(os.getenv('TOKEN'))