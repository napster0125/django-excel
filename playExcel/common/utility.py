import _thread
from .consumers import kryptos_leader_channel_push,echo_leader_channel_push

def pushChangesKrytposLeaderboard(rank_list):
	_thread.start_new_thread ( kryptos_leader_channel_push, (rank_list,) )
	return

def pushChangesEchoLeaderboard(rank_list):
	_thread.start_new_thread ( echo_leader_channel_push, (rank_list,) )
	return

	