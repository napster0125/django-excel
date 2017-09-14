from django.core.serializers.json import DjangoJSONEncoder
import json
from channels import Group



def conn_user_count_channel(message):
	Group('user-count-channel').add(message.reply_channel)
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