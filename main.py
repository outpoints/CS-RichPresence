import time
import psutil
from pypresence import Presence
import server

client_id = '1151973828633829447'
game_time = None
RPC = Presence(client_id)  #start RPC
RPC.connect()  #start handshake with the loop
data = None
last_data = None  #cacheing data. Less requests to the rpc server

server = server.GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()

maps = ['de_dust2', 'de_ancient', 'de_mirage', 'de_anubis', 'de_inferno', 'de_nuke', 'de_train',
        'de_overpass', 'de_vertigo', 'cs_office', 'cs_italy', 'de_basalt', 'de_eden',
        'de_palais', 'de_whistle', 'ar_baggage', 'ar_shoots', 'ar_pool_day']

map_names = {
    'de_dust2': 'Dust II', 'de_ancient': 'Ancient', 'de_mirage': 'Mirage', 'de_anubis': 'Anubis',
    'de_inferno': 'Inferno', 'de_nuke': 'Nuke', 'de_train': 'Train', 'de_overpass': 'Overpass',
    'de_vertigo': 'Vertigo', 'cs_office': 'Office', 'cs_italy': 'Italy', 'de_basalt': 'Basalt',
    'de_eden': 'Eden', 'de_palais': 'Palais', 'de_whistle': 'Whistle', 'ar_baggage': 'Baggage',
    'ar_shoots': 'Shoots', 'ar_pool_day': 'Pool Day',
}

gamemode_mapping = {
    'deathmatch': 'Deathmatch', 'competitive': 'Competitive', 'gungameprogressive': 'Arms Race',
    'scrimcomp2v2': 'Wingman', 'casual': 'Casual', 'custom': 'Custom',
}

def gameRunning(): #faster way of checking process according to this: https://psutil.readthedocs.io/en/latest/#psutil.process_iter
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() in ('cs2', 'cs2.exe'):
            return True
    return False

while True:
    if gameRunning():
        if game_time is None: game_time = time.time() #set time at first time running

        player_activity = server.get_info("player", "activity")
        player_name = server.get_info("player", "steamid")
        local_player = server.get_info("provider", "steamid")
        map_name = server.get_info("map", "name")
        display_map_name = map_names.get(map_name, map_name)
        gamemode_name = server.get_info("map", "mode")
        display_gamemode = gamemode_mapping.get(gamemode_name, gamemode_name)

        if player_activity == 'menu':
            data = {
                "large_image": 'cs2',
                "state": "In Menu",
                "start": game_time
            }
            sleepTime = 2  #faster updates in the menu
        else:
            map_ct_score = server.get_info("map", "team_ct", "score")
            map_t_score = server.get_info("map", "team_t", "score")
            player_assists = server.get_info("player", "match_stats", "assists")
            player_kills = server.get_info("player", "match_stats", "kills")
            player_deaths = server.get_info("player", "match_stats", "deaths")
            player_team = server.get_info("player", "team")

            data = {
                "state": f'K: {player_kills} | D: {player_deaths} | A: {player_assists}'
                         if player_name == local_player else 'Dead',
                "details": f"{display_map_name} - {map_ct_score}:{map_t_score}"
                           if player_team == 'CT' else f"{display_map_name} - {map_t_score}:{map_ct_score}",
                "large_image": map_name if map_name in maps else 'unknown',
                "large_text": f"Playing {display_gamemode} on {display_map_name}",
                "small_image": 'ct' if player_team == 'CT' else 't',
                "small_text": f"Playing {player_team}",
                "start": game_time
            }
            sleepTime = 5  #slower updates, but could help with preformance
#refactor of edge cases
    else:  #game closed: reset data and game_time
        data = None
        game_time = None
        sleepTime = 10  #longer interval when game isn't running

    #update only if data doesnt match last_data
    if data != last_data:
        if data:
            RPC.update(**data)
        else:
            RPC.clear()
        last_data = data

    time.sleep(sleepTime) #changes based on if the game is open or not
