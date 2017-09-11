import _thread
from .consumers import kryptos_leader_channel_push

def pushChangesKrytposLeaderboard(rank_list):
	_thread.start_new_thread ( kryptos_leader_channel_push, (rank_list,) )
	return


	