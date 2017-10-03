from channels.routing import route
from . import consumers
channel_routing = [
	route('websocket.connect',
    	consumers.conn_kryptos_leader_channel,
    	path = r'^/leaderboard/kryptos'
     	),
	
	route('websocket.disconnect',
		consumers.disconn_kryptos_leader_channel,
		path = r'^/leaderboard/kryptos',
     	),
	route('websocket.connect',
    	consumers.conn_echo_leader_channel,
    	path = r'^/leaderboard/echo'
     	),
	
	route('websocket.disconnect',
		consumers.disconn_echo_leader_channel,
		path = r'^/leaderboard/echo',
     	),

	route('websocket.connect',
    	consumers.conn_user_count_channel,
    	path = r'^/getUserCount'
     	),
	
	route('websocket.disconnect',
		consumers.disconn_user_count_channel,
		path = r'^/getUserCount',
     	),


	route('websocket.connect',
    	consumers.connect_to_user_channel,
    	path = r'^/userChannel/'
     	),
	route('websocket.disconnect',
		consumers.disconnect_from_user_channel,
		path = r'^/userChannel/'
     	),

	route('websocket.connect',
    	consumers.conn_hashinclude_channel,
    	path = r'^/hashinclude/submissions'
     	),
	route('websocket.disconnect',
		consumers.disconn_hashinclude_channel,
		path = r'^/hashinclude/submissions'
     	),


	route('websocket.connect',
    	consumers.test_conn,
    	path = r'^/test'
     	),
	route('websocket.disconnect',
		consumers.test_disconn,
		path = r'^/test'
     	),


	]
