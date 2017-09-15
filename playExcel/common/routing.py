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
     	),
	route('websocket.connect',
    	consumers.conn_echo_leader_channel,
    	path = r'^/echo'
     	),
	
	route('websocket.disconnect',
		consumers.disconn_echo_leader_channel,
		path = r'^/echo',
     	),

	route('websocket.connect',
    	consumers.conn_user_count_channel,
    	path = r'^/getUserCount'
     	),
	
	route('websocket.disconnect',
		consumers.disconn_user_count_channel,
		path = r'^/getUserCount',
     	),
	]
