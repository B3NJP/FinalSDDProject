import math
import functions, exampleArts

def warrior(user, map, player): # Moves three spaces a turn, then attacks
    if not (player.loc[0] == user.loc[0] and player.loc[1] == user.loc[1]): # Only moves when not adjacent
        path = functions.pathFind(map, user.loc, player.loc)
        if path:
            user.loc = path[min(len(path)-1,2)] # Move to end of path or 3 spaces, whichever is smaller
    if (abs(player.loc[0] - user.loc[0])+abs(player.loc[1] - user.loc[1]) <= 1): # If (now) next to player, attack!
        functions.dealBasicDamage(user, player, [], 'PHY', 0) 
    
    