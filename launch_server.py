import server

# 1. Make HTTP POST to CSGO using the Game State Integration found here - https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration
# 2. Parse the request and fetch only certain aspects of match
# 3. Post a discord message that updates on gamestate change

server = server.GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()

