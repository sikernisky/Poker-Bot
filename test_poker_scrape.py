"""
test_poker_scrape.py
Teddy Siker
April 10th, 2022

A module to test poker_scrape.py.
"""

import poker_scrape

def test_clean_ledger_data():
	"""
	Unit test for clean_ledger_data.
	"""

	#Test 1: Only one player in the ledger.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 -32000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':-32000}, "got " + str(result)

	#Test 2: Two players in the ledger.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 -32000\n'
	scraped_data += '\nManchin @ r122dmss2 DETAILS 4000 9500 20050 10000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':-32000, 'r122dmss2':10000}, "got " + str(result)

	#Test 3: Two players in the ledger with the same name and stats.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 -32000\n'
	scraped_data += '\nBiden @ uuu20uun DETAILS 10000 40000 30000 -32000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':-32000, 'uuu20uun':-32000}

	#Test 4: Three players in the ledger: two with the same name.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 -32000\n'
	scraped_data += '\nManchin @ r122dmss2 DETAILS 4000 9500 20050 10000\n'
	scraped_data += '\nBiden @ uuu20uun DETAILS 1000 90500 30000 60000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':-32000, 'r122dmss2':10000, 'uuu20uun':60000}	

	#Test 5: Player name is the same as a different player's ID.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 -32000\n'
	scraped_data += '\nncew021f21 @ r122dmss2 DETAILS 4000 9500 20050 10000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':-32000, 'r122dmss2':10000}

	#Test 6 (not realistic but necessary): All players go positive.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 32000\n'
	scraped_data += '\nManchin @ r122dmss2 DETAILS 4000 9500 20050 10000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':32000, 'r122dmss2':10000}

	#Test 7 (not realistic but necessary): All players go negative.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 -32000\n'
	scraped_data += '\nManchin @ r122dmss2 DETAILS 4000 9500 20050 -10000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':-32000, 'r122dmss2':-10000}

	#Test 8: All players go even.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 0\n'
	scraped_data += '\nManchin @ r122dmss2 DETAILS 4000 9500 20050 0\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':0, 'r122dmss2':0}

	#Test 9: Some players go even, some don't.
	scraped_data = '\nBiden @ ncew021f21 DETAILS 10000 40000 30000 1000\n'
	scraped_data += '\nManchin @ r122dmss2 DETAILS 3040 9500 20050 -5000\n'
	scraped_data += '\nSinema @ yavnXNmm29 DETAILS 4000 2 20050 0\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':1000, 'r122dmss2':-5000, 'yavnXNmm29':0}

	#Test 10: Many spaces between different information.
	scraped_data = '\nBiden @ cyyqm2241         DETAILS 10000  40000 30000 -90\n'
	scraped_data += '\nManchin @     pouw3lfq092 DETAILS   4000      9500  20050  1   \n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'cyyqm2241':-90, 'pouw3lfq092':1}

	#Test 11: Player names have spaces.
	scraped_data = '\nJoe Biden @ ncew021f21 DETAILS 10000 40000 30000 40000\n'
	scraped_data += '\nJoe Manchin @ r122dmss2 DETAILS 4000 9500 20050 40000\n'
	result = poker_scrape.clean_ledger_data(scraped_data)
	assert result == {'ncew021f21':40000, 'r122dmss2':40000}


	print('Passed Unit Test: test_clean_ledger_data()')


if __name__ == '__main__':
	"""
	Runs all unit tests.
	"""
	test_clean_ledger_data()