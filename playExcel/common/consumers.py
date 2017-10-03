from django.core.serializers.json import DjangoJSONEncoder
import json
from channels import Group
from channels.auth import http_session_user
import redis
redis_conn = redis.Redis("localhost", 6379)


def conn_user_count_channel(message):
	Group('user-count-channel').add(message.reply_channel)
	print("conntendffhbdf")
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	return 


def disconn_user_count_channel(message):
	Group('user-count-channel').discard(message.reply_channel)


def user_count_channel_push(data):
    Group('user-count-channel').send( 
		{
			'text': json.dumps(data,cls=DjangoJSONEncoder)
		})

def conn_kryptos_leader_channel(message):
	Group('kryptos-leader-channel').add(message.reply_channel)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	print("New kryptos listener added!")


def disconn_kryptos_leader_channel(message):
	Group('kryptos-leader-channel').discard(message.reply_channel)


def kryptos_leader_channel_push(data):
    Group('kryptos-leader-channel').send( 
		{
			'text': json.dumps(data,cls=DjangoJSONEncoder)
		})


def conn_echo_leader_channel(message):
	Group('echo-leader-channel').add(message.reply_channel)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	print("New echo listener added!")


def disconn_echo_leader_channel(message):
	Group('echo-leader-channel').discard(message.reply_channel)


def echo_leader_channel_push(data):
    Group('echo-leader-channel').send( 
		{
			'text': json.dumps(data,cls=DjangoJSONEncoder)
		})





@http_session_user
def connect_to_user_channel(message):
	try:
		userid = message.http_session['user']
		redis_conn.hset("online-users",
			userid,
			message.reply_channel.name)
		print('New user listener added!')
	except:
		print("user not logged in, can't connect to user channel!")
		pass


@http_session_user
def disconnect_from_user_channel(message):
	try:
		userid = message.http_session['user']
		redis_conn.hdel("online-users",userid)
	except:
		pass


def userDataPush(userid,data):
	Channel( redis_conn.hget("online-users",userid) ).send(
		{
		'text' : json.dumps(sellData,cls=DjangoJSONEncoder)
		}
	)






def conn_hashinclude_channel(message):
	Group('hashinclude-channel').add(message.reply_channel)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	return 


def disconn_hashinclude_channel(message):
	Group('hashinclude-channel').discard(message.reply_channel)


def hashinclude_channel_push(data):
	Group('hashinclude-channel').send( 
		{
			'text': json.dumps(data,cls=DjangoJSONEncoder)
		})






def disconnectAll(userid):
	redis_conn.hdel("online-users",userid)




@http_session_user
def test_conn(message):
	print("channel subs: ",message.http_session['count'])
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{ "close" : True }
		})
	return

def test_push(data):
	pass 


def test_disconn(message):
	pass