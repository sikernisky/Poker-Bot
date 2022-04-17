"""
test_poker.py
Teddy Siker
April 10th, 2022

Complete test suite for the PokerBot.
"""

import poker_scrape
import poker_save
import game

def test_update_stats():
	"""
	Unit test for update_stats.
	"""

	#Test 1: Old stats and new stats are empty.
	new_stats = {}
	old_stats = {}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {}, "test failed, got " + repr(result)

	#Test 2: Old stats is empty, new stats is not.
	new_stats = {'xsoe3i9smmn2':100000}
	old_stats = {}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':100000}, "test failed, got " + repr(result)

	#Test 3: Old stats is not empty, new stats is.
	new_stats = {}
	old_stats = {'xsoe3i9smmn2':100000}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':100000}, "test failed, got " + repr(result)

	#Test 4: Old stats and new stats have the same players.
	new_stats = {'xsoe3i9smmn2':-30000}
	old_stats = {'xsoe3i9smmn2':100000}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':70000}, "test failed, got " + repr(result)

	#Test 5: Old stats and new stats have different players.
	new_stats = {'uoppp7842':1000}
	old_stats = {'xsoe3i9smmn2':45050}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':45050,'uoppp7842':1000}, "test failed, got " + repr(result)

	#Test 6: Old stats and new stats have same AND different players.
	new_stats = {'uoppp7842':1000}
	old_stats = {'xsoe3i9smmn2':45050, 'uoppp7842':1000}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':45050,'uoppp7842':2000}, "test failed, got " + repr(result)

	#Test 7: Everyone's net balance increases.
	new_stats = {'uoppp7842':400, 'xsoe3i9smmn2':5000}
	old_stats = {'xsoe3i9smmn2':45050, 'uoppp7842':1000}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':50050,'uoppp7842':1400}, "test failed, got " + repr(result)

	#Test 8: Everyone's net balance decreases.
	new_stats = {'uoppp7842':-1900, 'xsoe3i9smmn2':-100}
	old_stats = {'xsoe3i9smmn2':45050, 'uoppp7842':1000}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':44950,'uoppp7842':-900}, "test failed, got " + repr(result)

	#Test 9: Everyone's net balance stays the same.
	new_stats = {'uoppp7842':0, 'xsoe3i9smmn2':0}
	old_stats = {'xsoe3i9smmn2':45050, 'uoppp7842':1000}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':45050,'uoppp7842':1000}, "test failed, got " + repr(result)

	#Test 10: Some net balances increase, decrease, and stay the same.
	new_stats = {'uoppp7842':100000, 'xsoe3i9smmn2':0, 'ppouyzm09tianz':-502}
	old_stats = {'xsoe3i9smmn2':45050, 'uoppp7842':1000, 'ppouyzm09tianz':502}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':45050,'uoppp7842':101000, 
	'ppouyzm09tianz':0}, "test failed, got " + repr(result)

	#Test 11: Old stats has more players than new stats.
	new_stats = {'uoppp7842':10000, 'xsoe3i9smmn2':500}
	old_stats = {'xsoe3i9smmn2':45050, 'uoppp7842':1000, 'ppouyzm09tianz':900500}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':45550,'uoppp7842':11000, 'ppouyzm09tianz':900500}, "test failed, got " + repr(result)

	#Test 12: New stats has more players than old stats.
	new_stats = {'uoppp7842':10000, 'xsoe3i9smmn2':-2000, 'ppouyzm09tianz':900500}
	old_stats = {'xsoe3i9smmn2':45050, 'uoppp7842':1000}
	result = poker_save.update_stats(new_stats, old_stats)
	assert result == {'xsoe3i9smmn2':43050,'uoppp7842':11000, 'ppouyzm09tianz':900500}, "test failed, got " + repr(result)

	print('Passed Unit Test: test_update_stats()')


def test_different_ids():
	"""
	Unit test for different_ids.
	"""

	#Test 1: Both lists have one different ID.
	net_ids = ['oajg330mf3z']
	people_ids = ['drkow9s21']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == ['oajg330mf3z'], "failed, got " + repr(result)

	#Test 2: Both lists have one (same) ID.
	net_ids = ['oajg330mf3z']
	people_ids = ['oajg330mf3z']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == [], "failed, got " + repr(result)

	#Test 3: Both lists have two IDs, both different.
	net_ids = ['oajg330mf3z', 'sl021mx33']
	people_ids = ['drkow9s21', 'po29mmol3vv']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == ['oajg330mf3z', 'sl021mx33'], "failed, got " + repr(result)

	#Test 4: Both lists have two IDS, both same.
	net_ids = ['oajg330mf3z', 'sl021mx33']
	people_ids = ['oajg330mf3z', 'sl021mx33']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == [], "failed, got " + repr(result)	

	#Test 5: Both lists have two IDS, one different and one same.
	net_ids = ['oajg330mf3z', 'sl021mx33']
	people_ids = ['oajg330mf3z', 'po29mmol3vv']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == ['sl021mx33'], "failed, got " + repr(result)

	#Test 6: Net_id list has only one ID, people_id list has two, both different.
	net_ids = ['oajg330mf3z', 'sl021mx33']
	people_ids = ['po29mmol3vv']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == ['oajg330mf3z', 'sl021mx33'], "failed, got " + repr(result)

	#Test 7: People_id list has only one ID, net_id list has two, both different.
	net_ids = ['oajg330mf3z']
	people_ids = ['po29mmol3vv', 'sl021mx33']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == ['oajg330mf3z'], "failed, got " + repr(result)

	#Test 8: People_id list has only one ID, net_id list has two, one same ID.
	net_ids = ['oajg330mf3z', 'sl021mx33']
	people_ids = ['oajg330mf3z']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == ['sl021mx33'], "failed, got " + repr(result)

	#Test 9: Net_id list has only one ID, people_id list has two, one same ID.
	net_ids = ['oajg330mf3z']
	people_ids = ['oajg330mf3z','sl021mx33']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == [], "failed, got " + repr(result)	

	#Test 10: Both lists have two IDs, same ones except for one character.
	net_ids = ['oajg330mf3T', 'sl021mx3T']
	people_ids = ['oajg330mf3z', 'sl021mx33']
	result = poker_save.different_ids(net_ids, people_ids)
	assert result == ['oajg330mf3T', 'sl021mx3T'], "failed, got " + repr(result)

	print('Passed Unit Test: test_different_ids()')


def test_valid_url():
	"""
	Unit test for valid_url.
	"""

	#Test 1: url is an empty string.
	url = ''
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)

	#Test 2: url is a string with one character.
	url = '/'
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)

	#Test 3: url is just the PokerNow url stub (https://www.pokernow.club/games/)
	url = 'https://www.pokernow.club/games/'
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)

	#Test 4: url is valid but has a missing slash in its stub
	url = 'https:/www.pokernow.club/games/pglMvypJMlx4MgcBmnRRNMn0S'
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)

	#Test 5: url is valid but has a missing slash at the end of its stub
	url = 'https:/www.pokernow.club/gamespglMvypJMlx4MgcBmnRRNMn0S'
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)

	#Test 6: url has a valid stub but invalid game ID
	url = 'https:/www.pokernow.club/games/pglMvypJOQIjoemanchinEGHVIwe9Q023GJFVnjoebidenBmnRRNMn0S'
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)

	#Test 7: url is a string with more than one character.
	url = 'hi'
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)

	#Test 8: url is a valid game ID.
	url = 'https://www.pokernow.club/games/pglMvypJMlx4MgcBmnRRNMn0S'
	result = poker_scrape.valid_url(url)
	assert result == True, 'failed: got ' + repr(result)

	#Test 9: url is a valid game ID with one character missing, making it invalid.
	url = 'https://www.pokernow.club/games/pglMypJMlx4MgcBmnRRNMn0S'
	result = poker_scrape.valid_url(url)
	assert result == False, 'failed: got ' + repr(result)	

	print('Passed Unit Test: test_valid_url()')


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

def test_compute_stats():
	"""
	Unit test for compute_stats.
	"""

	#Test 1: prev_stats and prev_people are empty.
	prev_stats = {}
	prev_people = {}
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {}, "failed: got " + repr(result)

	#Test 2: prev_stats is empty, prev_people is not.
	prev_stats = {}
	prev_people = {'jj31nnaln3qm':'1235912213'}
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 0}, "failed: got " + repr(result)

	#Test 3: prev_stats and prev_people have the same PokerNow ID.
	prev_stats = {'jj31nnaln3qm': 50000}
	prev_people = {'jj31nnaln3qm':'1235912213'}
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 50000}, "failed: got " + repr(result)

	#Test 4: prev_people has two PokerNow IDs that correspond to the same person.
	#		 prev_stats only lists one of those IDs.
	prev_stats = {'jj31nnaln3qm': 50000}
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'1235912213' }
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 50000}, "failed: got " + repr(result)

	#Test 5: prev_people has two PokerNow IDs that correspond to the same person.
	#		 prev_stats lists both of those IDs.
	prev_stats = {'jj31nnaln3qm': 50000, 'iowlxz2oiwj1' : 70000}
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'1235912213' }
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 120000}, "failed: got " + repr(result)

	#Test 6: repeat of above test but with negative net balances.
	prev_stats = {'jj31nnaln3qm': -50000, 'iowlxz2oiwj1' : -70000}
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'1235912213' }
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : -120000}, "failed: got " + repr(result)

	#Test 7: repeat of above test but with one positive and one negative net balance.
	prev_stats = {'jj31nnaln3qm': -50000, 'iowlxz2oiwj1' : 70000}
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'1235912213' }
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 20000}, "failed: got " + repr(result)

	#Test 8: prev_stats and prev_people have two different PokerNow IDs and Discord IDs.
	prev_stats = {'jj31nnaln3qm': 50000, 'iowlxz2oiwj1' : 70000}
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'9990410851' }
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 50000, '9990410851':70000}, "failed: got " + repr(result)

	#Test 9: prev_people has two PokerNow IDs that correspond to the same person and
	#		 one other PokerNow ID.
	prev_stats = {'jj31nnaln3qm': 50000}
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'9990410851' }
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 50000, '9990410851':0}, "failed: got " + repr(result)

	#Test 10: prev_people has two PokerNow IDs that correspond to one person and two
	#		 PokerNow IDs that correspond to another person.
	prev_stats = {'jj31nnaln3qm': 50000, 'iowlxz2oiwj1' : 0, 'jq13tjgm1q1' : 90500 }
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'9990410851', 'jq13tjgm1q1':'9990410851'}
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 50000, '9990410851':90500}, "failed: got " + repr(result)

	#Test 11: prev_stats isn't empty, prev_people is.
	prev_stats = {'jj31nnaln3qm': 50000, 'iowlxz2oiwj1' : 0, 'jq13tjgm1q1' : 90500 }
	prev_people = {}
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {}, "failed: got " + repr(result)

	#Test 12: prev_stats and prev_people have one element : different PokerNow ID.
	prev_stats = {'jj31nnaln3qm': 50000}
	prev_people = {'iowlxz2oiwj1':'9990410851' }
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'9990410851': 0}, "failed: got " + repr(result)

	#Test 13: prev_stats and prev_people have two elements with different PokerNow IDs.
	prev_stats = {'jj31nnaln3qm': 50000, 'iowlxz2oiwj1' : 0}
	prev_people = {'jq13tjgm1q1':'1235912213', 'awe9gh123d':'1250775'}
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213':0, '1250775':0}, "failed: got " + repr(result)

	#Test 14: prev_stats has one more & different element than prev_people, which has two elements.
	prev_stats = {'jj31nnaln3qm': 50000, 'iowlxz2oiwj1' : 0, 'jq13tjgm1q1' : 90500 }
	prev_people = {'jj31nnaln3qm':'1235912213', 'iowlxz2oiwj1':'9990410851'}
	result = poker_save.compute_stats(prev_stats, prev_people)
	assert result == {'1235912213' : 50000, '9990410851':0}, "failed: got " + repr(result)

	print('Passed Unit Test: test_compute_stats()')

def test_sort_stats():
	"""
	Unit test for sort_stats.
	"""

	#Test 1: empty dictionary
	stats = {}
	result = game.sort_stats(stats)
	assert result == {}, "failed: got " + repr(result)

	#Test 2: one element in dictionary
	stats = {'198762987632':2000}
	result = game.sort_stats(stats)
	assert result == {'198762987632':2000}, "failed: got " + repr(result)

	#Test 3: two elements, already sorted
	stats = {'79120777732':50000, '198762987632':2000}
	result = game.sort_stats(stats)
	assert result == {'79120777732':50000, '198762987632':2000}, "failed: got " + repr(result)

	#Test 4: two elements, not sorted
	stats = {'198762987632':2000, '79120777732':50000}
	result = game.sort_stats(stats)
	assert result == {'79120777732':50000, '198762987632':2000}, "failed: got " + repr(result)

	#Test 5: two elements, same net value
	stats = {'198762987632':2000, '79120777732':2000}
	result = game.sort_stats(stats)
	assert result == {'198762987632':2000, '79120777732':2000}, "failed: got " + repr(result)

	#Test 6: three elements, all wrong order
	stats = {'198762987632':2000, '79120777732':20000, '61526681463':107050}
	result = game.sort_stats(stats)
	assert result == {'61526681463':107050, '79120777732':20000, '198762987632':2000}, "failed: got " + repr(result)

	#Test 7: three elements, first is correct, others are not
	stats = {'61526681463':107050, '198762987632':2000, '79120777732':20000, }
	result = game.sort_stats(stats)
	assert result == {'61526681463':107050, '79120777732':20000, '198762987632':2000}, "failed: got " + repr(result)

	#Test 8: three elements, second is correct, others are not
	stats = {'198762987632':2000, '79120777732':20000, '61526681463':107050, }
	result = game.sort_stats(stats)
	assert result == {'61526681463':107050, '79120777732':20000, '198762987632':2000}, "failed: got " + repr(result)

	#Test 9: three elements, last is correct, others are not
	stats = {'79120777732':20000, '61526681463':107050, '198762987632':2000,}
	result = game.sort_stats(stats)
	assert result == {'61526681463':107050, '79120777732':20000, '198762987632':2000}, "failed: got " + repr(result)

	#Test 10: sorting wrongly-ordered negative numbers with positive numbers
	stats = {'79120777732':-50000, '198762987632':2000}
	result = game.sort_stats(stats)
	assert result == {'198762987632':2000,'79120777732':-50000}, "failed: got " + repr(result)

	#Test 11: sorting wrongly-ordered negative numbers alone
	stats = {'79120777732':-50000, '198762987632':-30000}
	result = game.sort_stats(stats)
	assert result == {'198762987632':-30000,'79120777732':-50000}, "failed: got " + repr(result)

	print('Passed Unit Test: test_sort_stats')

def test_merge_stats():
	"""
	Unit test for merge_stats.
	"""

	#Test 1: two empty dictionaries
	s1 = {}
	s2 = {}
	result = poker_save.merge_stats(s1, s2)
	assert result == {}, "failed, got: " + repr(result)

	#Test 2: one empty dictionary, one non-empty
	s1 = {}
	s2 = {'eee3h1tnf2f' : 30000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'eee3h1tnf2f' : 30000}, "failed, got: " + repr(result)

	#Test 3: both dictionaries one element, same key
	s1 = {'eee3h1tnf2f' : 50000}
	s2 = {'eee3h1tnf2f' : 30000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'eee3h1tnf2f' : 80000}, "failed, got: " + repr(result)

	#Test 4: both dictionaries one element, different key
	s1 = {'eee3h1tnf2f' : 50000}
	s2 = {'iqfhnq277tm' : 10000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'eee3h1tnf2f' : 50000, 'iqfhnq277tm' : 10000}, "failed, got: " + repr(result)

	#Test 5: both dictionaries two elements, different keys
	s1 = {'eee3h1tnf2f' : 50000, 'gn3ahqp252' : 0}
	s2 = {'iqfhnq277tm' : 10000, 'cw3amnyk9' : 9000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'eee3h1tnf2f' : 50000, 'iqfhnq277tm' : 10000, 'gn3ahqp252':0,'cw3amnyk9':9000 }, "failed, got: " + repr(result)

	#Test 6: both dictionaries two elements, one same key
	s1 = {'eee3h1tnf2f' : 50000, 'gn3ahqp252' : 0}
	s2 = {'eee3h1tnf2f' : 10000, 'cw3amnyk9' : 9000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'eee3h1tnf2f' : 60000, 'gn3ahqp252':0,'cw3amnyk9':9000 },"failed, got: " + repr(result)

	#Test 7: both dictionaries two elements, both same keys
	s1 = {'eee3h1tnf2f' : 50000, 'gn3ahqp252' : 0}
	s2 = {'eee3h1tnf2f' : 10000, 'gn3ahqp252' : 9000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'eee3h1tnf2f' : 60000, 'gn3ahqp252':9000}, "failed, got: " + repr(result)

	#Test 8: both dictionaries two elements, same keys and values
	s1 = {'eee3h1tnf2f' : 10000, 'gn3ahqp252' : 0}
	s2 = {'eee3h1tnf2f' : 10000, 'gn3ahqp252' : 0}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'eee3h1tnf2f' : 20000, 'gn3ahqp252':0}, "failed, got: " + repr(result)

	#Test 9: both dictionaries two elements, negative values
	s1 = {'cw3amnyk9' : -10000, 'gn3ahqp252' : -100}
	s2 = {'eee3h1tnf2f' : -10000, 'gn3ahqp252' : -9000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'cw3amnyk9' : -10000, 'eee3h1tnf2f' : -10000, 'gn3ahqp252':-9100}, "failed, got: " + repr(result)

	#Test 10: both dictionaries two elements, one neg and one pos value
	s1 = {'cw3amnyk9' : -10000, 'gn3ahqp252' : 0}
	s2 = {'eee3h1tnf2f' : 10000, 'gn3ahqp252' : -9000}
	result = poker_save.merge_stats(s1, s2)
	assert result == {'cw3amnyk9' : -10000, 'eee3h1tnf2f' : 10000, 'gn3ahqp252':-9000}, "failed, got: " + repr(result)

	print('Passed Unit Test: test_merge_stats')


if __name__ == '__main__':
	"""
	Runs all unit tests.
	"""
	test_valid_url()
	test_update_stats()
	test_different_ids()
	test_clean_ledger_data()
	test_compute_stats()
	test_sort_stats()
	test_merge_stats()