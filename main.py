"""
"""
import poker_scrape
import poker_save
import os
import discord
from discord.ext import commands
import game
from dotenv import load_dotenv #Delete once on Heroku
from discord.ext import tasks


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
	game.PokerGame.new_ids = ['biden', 'manchin']
	await poll_members(ctx)


@client.command()
async def stats(ctx):
	"""
	"""
	if game.PokerGame.current_game == None:
		await game.print_poker_stats(ctx, client, poker_save.stats())
	elif game.PokerGame.new_ids != []:
		await ctx.send("Please assign players so that my stats are accurate.")
	else:
		await ctx.send("Please give me a moment while I scrape live PokerNow data. . .")
		nets = await game.PokerGame.current_game.live_nets()
		print(type(nets))
		computed = poker_save.compute_stats(nets, poker_save.previous_people())
		await game.print_poker_stats(ctx, client, computed)



@client.command()
async def wipe(ctx):
	"""
	"""
	poker_save.wipe_files()
	await ctx.send("Wiped files.")


# @tasks.loop(seconds=25)
# async def refresh():
# 	if game.PokerGame.current_game != None and game.PokerGame.update_ctx != None:
# 		scraped_data = poker_scrape.scrape_ledger_data(game.PokerGame.current_game.url)
# 		poker_save.update_all_balances(scraped_data)
# 		game.PokerGame.new_ids = poker_save.foreign_poker_ids()
# 		await poll_members(game.PokerGame.update_ctx)



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

	if game.PokerGame.current_game != None:
		await game.PokerGame.current_game.immortalize()
		time.sleep(5)
		game.PokerGame.current_game = None

	player_discord_ids = []
	prev_players = poker_save.previous_people()
	for k in prev_players:
		player_discord_ids.append(prev_players[k])

	tracked_game = game.PokerGame(player_discord_ids, url)
	game.PokerGame.update_ctx = ctx

	await tracked_game.live_nets()

	#If there is a game already being tracked, write the Nets.



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

	if game.PokerGame.id_query == '': #Someone types !assign but PokerBot isn't polling
		await ctx.send("I am not currently matching PokerNow IDs with Discord members.")
		return

	if member == None:
		await ctx.send("That member does not exist in this server. Please try again.")

	poker_save.add_player(game.PokerGame.id_query, str(member.id))

	await ctx.send("I assigned the PokerNow ID: **" + game.PokerGame.id_query + "** to " + member.name  + ".")
	game.PokerGame.id_query = ''
	await game.PokerGame.current_game.poll_members(ctx)



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


client.run(os.getenv('TOKEN'))