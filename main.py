#!/usr/bin/env python3

import time

import psutil
from pypresence import Presence
import server

client_id = '1151973828633829447'

game_time = None
game_running = False

RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop
data = None

server = server.GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()

maps = ['de_dust2', 'de_ancient', 'de_mirage', 'de_anubis', 'de_inferno', 'de_nuke', 'de_train', #active duty
        'de_overpass', 'de_vertigo', #reserve pool
        'cs_office', 'cs_italy', 'cs_agency', #hostage maps
        'de_grail', 'de_jura', #communuity group
        'de_brewry', 'de_dogtown', #wingman
        'ar_baggage', 'ar_shoots', 'ar_pool_day', #arms race

        'de_palais', 'de_whistle', 'de_basalt', 'de_eden', #inactive maps
        ]

map_names = {#active duty
             'de_dust2': 'Dust II', 
             'de_ancient': 'Ancient', 
             'de_mirage': 'Mirage', 
             'de_anubis': 'Anubis', 
             'de_inferno': 'Inferno', 
             'de_nuke': 'Nuke', 
             'de_train': 'Train',
             
             #reserve pool
             'de_overpass': 'Overpass',
             'de_vertigo': 'Vertigo',
             
             #hostage maps
             'cs_office': 'Office', 
             'cs_italy': 'Italy',
             'cs_agency': 'Agency',

             #community group
             'de_grail': 'Grail',
             'de_jura': 'Jura',

             #wingmang
             'de_brewry': 'Brewery', 
             'de_dogtown': 'Dogtown',
             
             #arms race
             'ar_baggage': 'Baggage',
             'ar_shoots': 'Shoots',
             'ar_pool_day': 'Pool Day',

             #inactive maps
             'de_palais': 'Palais', 
             'de_whistle': 'Whistle',
             'de_basalt': 'Basalt', 
             'de_eden': 'Eden',
             }

gamemode_mapping = {'deathmatch': 'Deathmatch',
                    'competitive': 'Competitive',
                    'gungameprogressive': 'Arms Race',
                    'scrimcomp2v2': 'Wingman',
                    'casual': 'Casual',
                    'custom': 'Custom',
                    }

while True:
    game_found = False  #flag to check if the game is currently running

    for proc in psutil.process_iter():
        match proc.name().lower():
            case "cs2" | "cs2.exe":
                game_found = True

                if game_time is None:  #only set time if it's the first detection
                    game_time = time.time()

                player_activity = server.get_info("player", "activity")
                player_name = server.get_info("player", "steamid")
                local_player = server.get_info("provider", "steamid")
                map_map = server.get_info("map", "name")
 
                print(f'{server.get_info("map", "name")}')
                #print(f'{server.get_info("player", "steamid")}')
                #print(f'{server.get_info("provider", "steamid")}')
                #print(f'{server.get_info("player", "match_stats", "kills")}')

                if player_activity == 'menu':
                    data = {"large_image": 'cs2',
                            "state": "In Menu", 
                            "start": game_time
                            }
                    time.sleep(1)

                if player_activity != 'menu':
                    #convert maps/gamemodes to array to get actual map/gamemode name instead of file name
                    map_name = server.get_info("map", "name")
                    display_map_name = map_names.get(map_name, map_name)
                    
                    gamemode_name = server.get_info("map", "mode")
                    display_gamemode = gamemode_mapping.get(gamemode_name, gamemode_name)

                    map_ct_score = server.get_info("map", "team_ct", "score")
                    map_t_score = server.get_info("map", "team_t", "score")
                    player_assists = server.get_info("player", "match_stats", "assists")
                    player_kills = server.get_info("player", "match_stats", "kills")
                    player_deaths = server.get_info("player", "match_stats", "deaths")
                    player_team = server.get_info("player", "team")

                    data = {"state": f'K: {player_kills} | D: {player_deaths} | A: {player_assists}' if player_name == local_player else f'Dead',
                            "details": f"{display_map_name} - {map_ct_score}:{map_t_score}" if player_team == 'CT' else f"{display_map_name} - {map_t_score}:{map_ct_score}",
                            "large_image": map_map if map_map in maps else 'unknown',
                            "large_text": f"Playing {display_gamemode} on {display_map_name}",
                            "small_image": 'ct' if player_team == 'CT' else 't',
                            "small_text": f"Playing {player_team}",
                            "start": game_time
                            }
                    time.sleep(1)
                break

            case _:
                data = None

    if data:
        RPC.update(**data)
    else:
        RPC.clear()
        game_time = None  #reset timer when the game is closed
        time.sleep(10)

    time.sleep(5)

