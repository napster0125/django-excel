from channels.routing import route
from . import consumers
channel_routing = [
	route('websocket.connect',
    	consumers.conn_kryptos_leader_channel,
    	path = r'^/kryptos'
     	),
	
	route('websocket.disconnect',
		consumers.disconn_kryptos_leader_channel,
		path = r'^/kryptos',
     	)
	]