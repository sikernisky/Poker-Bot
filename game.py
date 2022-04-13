"""
game.py
Teddy Siker
April 10th, 2022

Module to represent a poker game.
"""
import discord

class PokerGame(object):
	"""
	A class to represent a Poker Game.

	An instance represents this session's Poker Game.

	Class Attributes:
		- current_game [PokerGame] : the current PokerGame
		- claiming [bool] : if PokerBot is asking for Discord IDs

	Instance Attributes:
		- url [string] : this game's URL
		- players [string list] : discord IDs of players in the PokerGame
	"""

	current_game = None
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

		current_game = self