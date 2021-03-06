"""
poker_scrape.py
Teddy Siker
April 9th, 2022

Scrapes information from pokernow.com.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

gChromeOptions = webdriver.ChromeOptions()
gChromeOptions.headless = True
gChromeOptions.add_argument("disable-dev-shm-usage")
gChromeOptions.add_argument("--disable-dev-shm-usage")
gChromeOptions.add_argument("--no-sandbox")
gChromeOptions.add_argument("window-size=1400,745")



def valid_url(url):
	"""
	Returns: True if `url`, when pasted into the browser, links to a valid
	PokerNow game.
	"""
	if (not isinstance(url, str)):
		return False
	if url.find('https://www.pokernow.club/games/') != 0:
		return False

	response = str((requests.get(url)).content)
	return ('tos-agreement' not in response) and ('jitsi-container' in response)



def scrape_ledger_data(url):
	"""
	Returns: the raw, scraped ledger data from the PokerNow `url`.

	Parameter `url`: The PokerNow URL to scrape from.
	Precondition: `url` is a string and a valid PokerNow URL.
	"""
	assert valid_url(url), "Parameter url is not a valid PokerNow URL."

	#driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
	driver = webdriver.Chrome(options=gChromeOptions, executable_path=ChromeDriverManager().install())
	driver.get(url)
	wait = WebDriverWait(driver, 10)
	stats_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'show-log-button')))
	driver.execute_script("arguments[0].click();", stats_button)
	ledger_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'ledger-button')))
	driver.execute_script("arguments[0].click();", ledger_button)
	elem = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 
		'ledger-rows')))

	return clean_ledger_data(elem.text)

def clean_ledger_data(raw_data):
	"""
	Returns: a dictionary of player IDs and their net loss/gains.

	Parameter raw_data: The data scraped from PokerNow used to gather IDs and money.
	Precondition: raw_data is a string in the format:
		'[Player1 Chosen Name] @ [Player1 PokerNow ID]
		DETAILS
		[Buy In] [Buy Out] [Stack] +/-[Net]
		[Player2 Chosen Name] @ [Player2 PokerNow ID]
		DETAILS
		[Buy In] [Buy Out] [Stack] +/-[Net]
		TABLE TOTAL [Buy In] [Buy Out] [Stack]'

	Where no two players have the same PokerNow ID.

	The returned dictionary looks like:

	{Player1ID : Net, Player2ID : Net, ... }
	"""
	raw_data_spaces = ''
	on_backslash_n = False
	for i in raw_data:
		if i == '\n':
			raw_data_spaces += ' '
			raw_data_spaces += i
		else:
			raw_data_spaces += i

	split_by_line = raw_data_spaces.split('\n')
	details_removed = list(filter(('DETAILS ').__ne__, split_by_line))
	player_data_list = []
	data_str = ''
	counter = 0
	for i in details_removed:
		data_str += i
		if (counter+1) % 2 == 0:
			player_data_list.append(data_str)
			data_str = ''
		counter += 1


	result_dict = {}
	for player_data in player_data_list:
		player_id_start = player_data[player_data.rindex('@') + 2:]
		while player_id_start[0] == ' ':
			player_id_start = player_id_start[1:]
		player_id = player_id_start[:player_id_start.index(' ')]
		after_player_id = player_data[player_data.index(player_id) + len(player_id):]
		after_player_id = (after_player_id[1:len(after_player_id)]).strip()
		net = after_player_id[after_player_id.rindex(' '):]
		result_dict[player_id] = int(net)

	return result_dict