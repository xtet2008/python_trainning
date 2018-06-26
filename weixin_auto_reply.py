import requests
import itchat

KEY = '3be7cb2216f145d997e950b4aa7c7b0f'
PASSWORD = '55709085de222279'


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot'
    }

    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = "I received: " + msg['Text']
    reply = get_response(msg['Text'])
    print (msg['Text'])
    return reply or defaultReply


itchat.auto_login(hotReload=True)
itchat.run()