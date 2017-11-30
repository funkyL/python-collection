# Watcher script for tracking live dota league matches

import requests
from time import sleep, time, strftime

key = "" # steamapi key
league_id = 5157

params = { 'key': key, 'league_id' : league_id}
current_game_list = {} # match_id : running_time


class bcolors:
    OKGREEN = '\033[96m'
    END = '\x1b[0m'

def secs2string(secs):
	s = str(int(secs%60))
	m = str(int(secs/60))
	if len(s) == 1 : s = "0" + s
	if len(m) == 1 : m = "0" + m
	return m + ":" + s

def main():
	try:
		resp = requests.get('http://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/', params=params)
		games_json = resp.json()['result']['games']
	except:
		print("Retrying to connect to server..")
		return
	#print(resp.url)
	games_print = ['\033c','====' + strftime("%H:%M:%S") + '==============']
	for game in games_json:
		try:
			radiant = game['radiant_team']['team_name']
			dire = game['dire_team']['team_name']
			teams = radiant + " vs " + dire + ": "
		except:
			teams = "unknown teams"

		try:
			game_time = int(game['scoreboard']['duration'])
			timestamp = secs2string(game_time)
		except: timestamp = "-0:0"

	#try:
		p = 0
		match_id = game['match_id']
		if (timestamp == "00:00" or timestamp == "-0:0"):

			if match_id not in current_game_list.keys():
				new = bcolors.OKGREEN + "**NEW**  " + bcolors.END
				current_game_list[match_id] =  time()
	#except:
			else:
				new = bcolors.OKGREEN + secs2string(time()-current_game_list[match_id]) + bcolors.END + "    "
		else:
			new = "         "
			if match_id not in current_game_list.keys():
				current_game_list[match_id] = time()

		games_print.append(new + teams + " " + timestamp)

	if len(games_print) > 2:
		for line in games_print: print(line)

while True:
	main()
	sleep(18)
