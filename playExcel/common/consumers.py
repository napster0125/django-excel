from django.core.serializers.json import DjangoJSONEncoder
import json
from channels import Group



def conn_kryptos_leader_channel(message):
	Group('kryptos-leader-channel').add(message.reply_channel)
	message.reply_channel.send({
		'text' : json.dumps({"accept": True}) #{"close": True}
		})
	print("New kryptos listener added!")


def disconn_kryptos_leader_channel(message):
	Group('kryptos-leader-channel').discard(message.reply_channel)


def kryptos_leader_channel_push(data):
    Group('kryptos-leader-channel').send( 
		{
			'text': json.dumps(data,cls=DjangoJSONEncoder)
		})
