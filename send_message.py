from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

accound_sid = 'ACede8ef66bc79e37fe87f14f9f0775c32'
auth_token = 'ccc9d84575cbbdf9f73ee11744197491'
phone_from = '+19127334508'
phone_to = '+8618618458391'

client = Client(accound_sid, auth_token)




# r = VoiceResponse()
# r.say("Welcome to twilio!")
# print(str(r))

message = client.messages.create(to=phone_to, from_=phone_from, body="你好【张胜】，收到信息了吗？")

print('message.sid:\t', message.sid)

# call = twilioCli.calls.create(to=phone_to,
#                            from_=phone_from,
#                            url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient"
#                               )
# print(call.sid)

#
#
# input('pause')
# print('message.to:\t', message.to)     ##手机号 '+86180xxxxxxxx'
#
#
# input('pause')
# print('message.from_:\t', message.from_)  ##Twilio号码，下划线“_”区分关键字from    '+149xxxxxxxx'
#
# input('pause')
# print('message.body:\t', message.body) ##消息    'I want to see you.'
#
# input('pause')
# print('message.status:\t', message.status)   ##如果消息被创建和发送，date_created和date_sent属性都包含一个datetime对象。'queued'
#
# input('pause')
# print('message.date_created:\t', message.date_created)  # datetime.datetime(2018,2,19,20,58,18)
#
#
# input('pause')
# message.date_sent == None  ##先将message对象记录在message变量中，短信才实际发送，所以date_sent为None
#
# input('pause')
# print('message.sid:\t', message.sid)           ##每个Twilio消息都有唯一的字符串ID（SID），可以用于获取Message对象的最新更新。 ‘SMxxxxxxxxxxxxxxxxxx’
#
# input('pause')
# updatedMessage=twilioCli.messages.get(message.sid)     ##重新获取message对象。
#
# input('pause')
# print('updatedMessage.status:\t', updatedMessage.status) ##属性可以为：queued、sending、sent、delivered、undelivered或failed。'delivered'
#
# updatedMessage.date_sent  #datetime.datetime(2018,2,19,20,58,18)
# https://blog.51cto.com/juispan/2071903