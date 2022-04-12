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

def get_previous_stats():
	"""
	Returns: a dictionary of the latest stats from NET_FILE_NAME.

	This dictionary has:
		-key [string]: valid PokerNowID
		-value [int]: accumulated, saved net balance
	"""
	with open(NET_FILE_NAME, 'r') as f:
		data = json.load(f)
		f.close()
		return json.loads(data)

def get_previous_ids(file):
	"""
	Returns: a string list of the PokerNow IDs from `file`.

	Parameter file: The file with PokerNow IDs.
	Precondition: file is a valid path to a file with valid PokerNow IDs in JSON format.

	This dictionary has:
		- key [string] : discord id
		- value [string] : valid PokerNow ID
	"""
	with open(file, 'r') as f:
		data = json.load(f)
		f.close()
		dict_data =  json.loads(data)
		ids = []
		for key in dict_data:
			ids.append(key)
		return ids

def write_new_stats(new_stats):
	"""
	Writes the new stats to NET_FILE_NAME.

	Parameter new_stats: The newest/most up to date net balances.
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



def file_exists():
	"""
	Returns: True if NET_FILE_NAME exists in this Directory; False otherwise.
	"""
	try:
		open(NET_FILE_NAME)
		return True
	except:
		return False

def get_new_ids():
	"""
	Returns: a list of PokerNow IDS that do not exist in ID_FILE_NAME
	but exist in the current PokerNow game.

	This function returns a list of strings.
	"""
	nets = get_previous_stats()



def update_all_balances(scraped_data):
	"""
	Updates everyone's net balances and rewrites NET_FILE_NAME to reflect these
	new balances.

	Parameter scraped_data: The newest data from PokerNow.com.
	Precondition: scraped_data is a dictionary with:
		-key [string]: valid PokerNowID
		-value [int]: updated net loss/gain
	"""
	if not file_exists(): #This should only be called ONCE EVER, if at all
		with open ('stats.json', 'w') as f:
			f.write(json.dumps(scraped_data))
			f.close()

	prev_stats = get_previous_stats()
	updated_stats = update_stats(prev_stats, scraped_data)
	write_new_stats(updated_stats)



def get_foreign_ids():
	"""
	Returns: a list of PokerNow IDs that exist in NET_FILE_NAME but not in 
	ID_FILE_NAME.

	This function returns a list of strings.
	"""
	return different_ids(get_previous_ids(NET_FILE_NAME), get_previous_ids(ID_FILE_NAME))


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
