import json
from typing import Dict, Optional

import discord

# TODO: replace with actual database
LOGIN_CHANNELS_FILEPATH = "src/data/login_channels.json"


#----------------------------------------------------------------------------------------------
# GET LOGIN CHANNEL
#----------------------------------------------------------------------------------------------
def get_login_channel(guild: discord.Guild) -> Optional[discord.TextChannel]:
    login_channels: Dict[str, str] = {}
    with open(LOGIN_CHANNELS_FILEPATH) as f:
        try:
            login_channels = json.load(f)
        except:
            return None
    if str(guild.id) in login_channels:
        login_channel_id = int(login_channels[str(guild.id)])
        return guild.get_channel(login_channel_id)

#----------------------------------------------------------------------------------------------
# SET LOGIN CHANNEL
#----------------------------------------------------------------------------------------------
def set_login_channel(guild_id: int, channel_id: int):
    login_channels: Dict[str, str] = {}
    with open(LOGIN_CHANNELS_FILEPATH) as f:
        try:
            login_channels = json.load(f)
        except:
            pass
    login_channels[guild_id] = channel_id
    with open(LOGIN_CHANNELS_FILEPATH, 'w') as f:
        json.dump(login_channels, f)
        f.close()

