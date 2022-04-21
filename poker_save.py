"""
poker_save.py
Teddy Siker
April 10th, 2022

A module responsible for saving and manipulating data from save files.
"""
import json
import pymongo
import game

NET_FILE_NAME = 'stats.json'
ID_FILE_NAME = 'people.json'


def update_stats(new_stats,old_stats):
	"""
	Returns: a dictionary of PokerNow PlayerIDs and updated net balances.

	Parameter stat_dict: The dictionary of players and their newest net
	balances.

	Precondition: stat_dict is a dictionary with:
		-key [string]: valid PokerNowID
		-value [int]: latest net balance (nightly gain/loss)

	The returned dictionary has the same format.
	"""
	assert isinstance(old_stats, dict), "Parameter old stats must be a dictionary."
	assert isinstance(new_stats, dict), "Parameter new stats must be a dictionary."
	for k in old_stats:
		assert isinstance(k, str), "old stats must have string keys."
		assert isinstance(old_stats[k], int), "old stats must have int values."
	for k in new_stats:
		assert isinstance(k, str), "new stats must have string keys."
		assert isinstance(new_stats[k], int), "new stats must have int values."	


	updated_stats = old_stats

	for player_id in new_stats:
		if player_id not in old_stats:
			updated_stats[player_id] = new_stats[player_id]
		else:
			updated_stats[player_id] = old_stats[player_id] + new_stats[player_id]

	return updated_stats

def add_player(poker_id, discord_id):
	"""
	Adds a {PokerID : DiscordID} key:value pair to ID_FILE_NAME.
	"""
	prev_people = previous_people()
	prev_people[poker_id] = discord_id
	write_new_people(prev_people)


def previous_stats():
	"""
	Returns: a dictionary of the latest stats from NET_FILE_NAME.

	This dictionary has:
		-key [string]: valid PokerNow ID
		-value [int]: accumulated, saved net balance
	"""
	stats_documents = game.PokerGame.stats_collection.find({})
	result = {}
	for doc in stats_documents:
		for item in doc:
			if item != '_id:':
				result[item] = doc[item]

	print(result)

	return result

def wipe_files():
	"""
	Wipes all data in NET_FILE_NAME and ID_FILE_NAME.
	"""

	with open(NET_FILE_NAME, 'w') as f:
		json_stats = json.dumps({})
		f.write(json_stats)
		f.close()

	with open(ID_FILE_NAME, 'w') as f:
		json_stats = json.dumps({})
		f.write(json_stats)
		f.close()


def stats():
	"""
	Returns: a dictionary of Discord IDs and their total net gain/loss.

	This dictionary has:
		-key [string] : valid Discord ID
		-value [int] : total net balance
	"""
	prev_stats = previous_stats()
	prev_people = previous_people()

	return compute_stats(prev_stats, prev_people)


def compute_stats(prev_stats, prev_people):
	"""
	Returns: A dictionary of Discord IDs and their accumulated net gains/losses.

	Parameter prev_stats: All previous PokerNow IDs and their accumulated net gains/losses.
	Precondition: prev_stats is a dictionary:
		- key [str] : PokerNow ID
		- value [int] : accumulated net gain/loss

	Parameter prev_people: All previous PokerNow IDs and their corresponding Discord IDs.
	Precondition: prev_people is a dictionary:
		- key [str] : PokerNow ID
		- value [str] : Discord ID
	"""
	assert isinstance(prev_stats, dict), 'parameter prev_stats must be a dict.'
	assert isinstance(prev_people, dict), 'parameter prev_people must be a dict.'
	for k in prev_stats:
		assert isinstance(k, str), 'prev_stats must have string keys.'
		assert len(k) > 0, 'a valid PokerId must be length > 0.'
		assert isinstance(prev_stats[k], int), 'prev_stats must have int values.'
	for k in prev_people:
		assert isinstance(k, str), 'prev_people must have string keys.'
		assert len(k) > 0, 'a valid PokerId must be length > 0.'
		assert isinstance(prev_people[k], str), 'prev_people must have string keys.'
		assert len(prev_people[k]) > 0, 'a valid Discord ID must be length > 0.'
		for n in prev_people[k]:
			assert not n.isalpha(), 'valid discord ids only contain integers.'

	result = {}

	known_prev_stats = {}
	for k in prev_stats:
		if k in prev_people:
			known_prev_stats[k] = prev_stats[k]

	prev_stats = known_prev_stats

	for poker_id in prev_people:
		discord_id = prev_people[poker_id]
		result[discord_id] = 0

	for poker_id in prev_stats:
		corresponding_discord = prev_people[poker_id]
		result[corresponding_discord] += prev_stats[poker_id]

	return result


def previous_people():
	"""
	Returns: a dictionary of the latest people from ID_FILE_NAME.

	This dictionary has:
		-key [string]: valid PokerNow ID
		-value [string]: valid Discord ID	
	"""

	#Get from MongoDB.

	people_documents = game.PokerGame.people_collection.find({})
	result = {}
	for doc in people_documents:
		for item in doc:
			if isinstance(item, str):
				result[item] = doc[item]

	return result


	#Get from local Json.
	# with open(ID_FILE_NAME, 'r') as f:
	# 	data = json.load(f)
	# 	return data

def poker_ids_from_file(file):
	"""
	Returns: a string list of the PokerNow IDs from `file`.

	Parameter file: The file with PokerNow IDs.
	Precondition: file is a valid path to a file with valid PokerNow IDs in JSON format.
	"""
	with open(file, 'r') as f:
		data = json.load(f)
		f.close()
		ids = []
		for key in data:
			ids.append(key)
		return ids

def write_new_stats(new_stats):
	"""
	Writes `new_stats` to NET_FILE_NAME.

	Parameter new_stats: The newest/most up to date PokerNow IDs and their net balances.
	Precondition: new_stats is a dictionary:
		-key [string]: valid PokerNowID
		-value [int]: up to date net balance
	"""
	assert isinstance(new_stats, dict), "Parameter new stats must be a dictionary."
	for k in new_stats:
		assert isinstance(k, str), "new stats must have string keys."
		assert isinstance(new_stats[k], int), "new stats must have int values."	


	#write to MongoDB.
	if game.PokerGame.stats_collection != None:
		game.PokerGame.stats_collection.insert_one(new_stats)


def write_new_people(new_people):
	"""
	Writes `new_people` to ID_FILE_NAME.

	Parameter new_stats: The newest/most up to date PokerNow IDs and their Discord IDs.
	Precondition: new_people is a dictionary:
		-key [string]: valid PokerNow ID
		-key [string]: valid Discord ID
	"""
	assert isinstance(new_people, dict), "Parameter new stats must be a dictionary."
	for k in new_people:
		assert isinstance(k, str), "new stats must have string keys."
		assert isinstance(new_people[k], str), "new stats must have string values."	

	if game.PokerGame.people_collection != None:
		game.PokerGame.people_collection.insert_one(new_people)


def file_exists(file):
	"""
	Returns: True if NET_FILE_NAME exists in this Directory; False otherwise.

	Parameter file: The file to check.
	Precondition: file is a string.
	"""
	try:
		open(file)
		return True
	except:
		return False


def merge_stats(s1, s2):
	"""
	Returns: a dictionary with all key, value pairs of s1 and s2.
	If s1 and s2 share a key, their values are added together.

	The dictionary is:
		- key [str] : valid PokerNow ID
		- value [int] : accumulated net balance
	"""
	result = {}
	for k in s1:
		if k in result:
			result[k] += s1[k]
		else:
			result[k] = s1[k]

	for k in s2:
		if k in result:
			result[k] += s2[k]
		else:
			result[k] = s2[k]

	return result



def different_ids(net_ids, people_ids):
	"""
	Returns: a list of PokerNow IDs that exist in `net_ids` but not in 
	`people_ids`.

	Parameter net_ids: The PokerNow ids from the NET_FILE_NAME file.
	Precondition: people_ids is a nonempty list of nonempty strings.

	Parameter people_ids: The PokerNow ids from the ID_FILE_NAME file.
	Precondition: people_ids is a nonempty list of nonempty strings.

	This function returns a list of strings.
	"""
	new_ids = []
	for poker_id in net_ids:
		if poker_id not in people_ids:
			new_ids.append(poker_id)
	return new_ids
