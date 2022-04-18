"""
game.py
Teddy Siker
April 10th, 2022

Module to represent a poker game.
"""
import discord
import poker_scrape
import poker_save
from discord.ext import tasks

class PokerGame(object):
	"""
	A class to represent poker games on pokernow.com.

	An instance represents a PokerNow game.

	Class Attributes:
		- current_game [PokerGame] : the current PokerGame
		- id_query [str] : the current PokerNow ID PokerBot is asking to identify
		- new_ids [string list] : all PokerNow IDs PokerBot doesn't recognize.
		- update_ctx [discord.Context] : valid bot context.

	Instance Attributes:
		- url [string] : this game's URL
		- players [string list] : discord IDs of players in the PokerGame
	"""

	current_game = None
	update_ctx = None
	id_query = ''
	new_ids = []

	def __init__(self, players, url):
		"""
		Creates a PokerGame object.

		Parameter players: The players playing in this PokerGame.
		Precondition: players is a non-empty list of non-empty strings, each
		of which represents a valid discord.Member object.

		Parameter url: The PokerNow URL representing this PokerGame.
		Precondition: url is a valid PokerNow URL.
		"""

		assert isinstance(url, str), "Parameter url must be a string."
		for player_id in players:
			assert isinstance(player_id, str), "Parameter players is invalid."

		self.players = players
		self.url = url

		PokerGame.current_game = self


	async def live_nets(self):
		"""
		Returns: a dictionary of PokerNow IDs and their accumulated net balances
		INCLUDING this PokerGame.

		The dictionary returned is:
			- key [str] : valid PokerNow ID
			- value [int] : accumulated + live net balance
		"""
		live_data = poker_scrape.scrape_ledger_data(self.url)
		prev_ppl = poker_save.previous_people()
		PokerGame.new_ids = poker_save.different_ids(list(live_data.keys()), list(prev_ppl.keys()))
		if PokerGame.new_ids != []:
			await self.poll_members(PokerGame.update_ctx)
		else:
			print("Live data: " + str(live_data))
			print("Prev stats: " + str(poker_save.previous_stats()))
			combined = poker_save.update_stats(live_data, poker_save.previous_stats())
			print("Combined stats: " + str(combined))
			return combined


	async def poll_members(self, ctx):
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
			

	async def immortalize(self):
		"""
		Writes the live data from this PokerGame's url to the save files.
		"""
		poker_save.write_new_stats(await self.live_nets())




async def print_poker_stats(ctx, client, stats):
	"""
	Prints out `stats` to the server in a user-friendly format.

	Parameter ctx: The bot context.
	Precondition: ctx is a valid bot Context. 

	Parameter client: The server client.
	Precondition: client is a valid server Client.

	Parameter stats: The stats to print out.
	Precondition: stats is a dictionary:
		- key [str] : valid Discord ID
		- value [int] : accumulated net balance

	This function prints in the format:

	'
	LEADERBOARD:

	[king emoji] [Discord Member with highest net balance]: $[net balance]
	[2] [Discord Member with 2nd highest net balance]: $[net balance]
	[3] [Discord Member with 3rd highest net balance]: $[net balance]
	[4] [Discord Member with 4th highest net balance]: $[net balance]
	[..]
	'
	"""
	all_members = {}
	for g in client.guilds:
		for member in g.members:
			all_members[str(member.id)] = member.name

	sorted_stats = sort_stats(stats)

	name_dict = {}

	for k in sorted_stats:
		discord_name = ''
		try:
			discord_name = all_members[k]
		except:
			discord_name = 'User Id: ' + k
		name_dict[discord_name] = sorted_stats[k]

	counter = 1
	msg = '---------------------------------------------------------------------\n'
	for discord_member in name_dict:
		if counter == 1:
			msg += ('1. :crown:' + ' **' 
				+ discord_member + ': ' + str(name_dict[discord_member]) + ' credits**:crown:\n' )
		else:
			msg += (str(counter) + '. ' 
				+ discord_member + ': ' + str(name_dict[discord_member]) + ' credits\n' )
		counter += 1

	await ctx.send(msg + '---------------------------------------------------------------------')



def sort_stats(stats):
	"""
	Returns: a dictionary of Discord IDs and their accumulated net balances
	in sorted order.

	Parameter stats: The stats to sort.
	Precondition: stats is a dictionary:
		- key [str] : valid Discord ID
		- value [int] : accumulated net balance

	The returned dictionary is in the format:
		- key [str] : valid Discord ID
		- sorted value [int] : accumulated net balance
	"""
	sorted_stats_reversed = sorted(stats, key = lambda x:stats[x])
	sorted_stats = list(reversed(sorted_stats_reversed))

	result = {}
	counter = 0
	for poker_id in sorted_stats:
		result[poker_id] = stats[sorted_stats[counter]]
		counter += 1

	return result



