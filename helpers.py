
from nba_api.stats.static import players
import json
import os

import unicodedata

#----------------------------------------------------------------------- PLAYER PHOTO PULLS ---------------------------------------------------------------------

_cache = {}
def normalize_name(name):
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

def get_player_id(name):
    normalized = normalize_name(name)
    
    if normalized in _cache:
        return _cache[normalized]
    
    all_players = players.get_players()
    matched = [p for p in all_players if normalize_name(p['full_name']).lower() == normalized.lower()]
    
    if matched:
        _cache[normalized] = matched[0]['id']
        return matched[0]['id']
    
    _cache[normalized] = None
    return None
#----------------------------------------------------------------------- GET PHOTO FROM NBA TEMPLATE ---------------------------------------------------------------------

def get_headshot_url(name):
    player_id = get_player_id(name)
    if player_id:
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    return None









