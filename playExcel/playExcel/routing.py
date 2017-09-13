from channels.routing import include

from common.routing import channel_routing as common_cr

channel_routing = [
    include( common_cr, path=r'^/channel/leaderboard')
]