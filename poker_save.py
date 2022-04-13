"""
poker_save.py
Teddy Siker
April 10th, 2022

A module responsible for saving everyone's Poker stats.
"""
import json

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
	with open(NET_FILE_NAME, 'r') as f:
		data = json.load(f)
		return data

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
	Returns: a dictionary of Discord IDs and their total net gain/loss.

	Parameter prev_stats: The dictionary of PokerNow IDs and their net balances.
	Precondition: prev_stats is a dictionary with:
		-key [string]: valid PokerNowID
		-value [int]: updated net loss/gain

	Parameter prev_people: The dictionary of PokerNow IDs and their Discord IDs.
	Precondition: prev_people is a dictionary with:
		-key [string]: valid PokerNow ID
		-value [string]: valid Discord ID

	Precondition: every PokerNow ID in `prev_stats` must be a key in `prev_people`.

	The returned dictionary has:
		-key [string]: valid PokerNow ID
		-value [int]: accumulated, saved net balance
	"""
	for k in prev_stats:
		assert k in prev_people, "Every key in prev_stats must be in prev_people."

	result = {}

	for k in prev_people:
		if k not in prev_stats:
			result[prev_people[k]] = 0
		else:
			result[prev_people[k]] = prev_stats[k]

	return result


def previous_people():
	"""
	Returns: a dictionary of the latest people from ID_FILE_NAME.

	This dictionary has:
		-key [string]: valid PokerNow ID
		-value [string]: valid Discord ID	
	"""
	with open(ID_FILE_NAME, 'r') as f:
		data = json.load(f)
		return data

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

	with open(NET_FILE_NAME, 'w') as f:
		json_stats = json.dumps(new_stats)
		f.write(json_stats)
		f.close()

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

	with open(ID_FILE_NAME, 'w') as f:
		json_stats = json.dumps(new_people)
		f.write(json_stats)
		f.close()


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


def update_all_balances(scraped_data):
	"""
	Updates everyone's net balances and rewrites NET_FILE_NAME to reflect these
	new balances.

	Parameter scraped_data: The newest data from PokerNow.com.
	Precondition: scraped_data is a dictionary with:
		-key [string]: valid PokerNowID
		-value [int]: updated net loss/gain
	"""
	if not file_exists(NET_FILE_NAME): #This should only be called ONCE EVER, if at all
		with open (NET_FILE_NAME, 'x') as f:
			f.write(json.dumps(scraped_data))
			f.close()
	if not file_exists(ID_FILE_NAME): #This should only be called ONCE EVER, if at all
		with open (ID_FILE_NAME, 'x') as f:
			f.write(json.dumps({}))
			f.close()


	prev_stats = previous_stats()
	updated_stats = update_stats(prev_stats, scraped_data)
	write_new_stats(updated_stats)




def foreign_poker_ids():
	"""
	Returns: a list of PokerNow IDs that exist in NET_FILE_NAME but not in 
	ID_FILE_NAME.

	This function returns a list of strings.
	"""
	return different_ids(poker_ids_from_file(NET_FILE_NAME), poker_ids_from_file(ID_FILE_NAME))


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
