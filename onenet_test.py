import requests
import struct

DEVICE_ID = '35234481'
API_KEY = 'YgZpr=pVTTU5KJ0=rW3sksjGVb4='

# _open = [0x95, 0x01, 0x02, 0x19, 0xA2, 0xB1, 0x00, 0x02, 0x83, 0x00, 0x00, 0x00, 0x3C, 0x40, 0x03, 0x00, 0x03, 0x02, 0x01, 0x01, 0xF6]
# _close = [0x95, 0x01, 0x02, 0x19, 0xA2, 0xB1, 0x00, 0x02, 0x83, 0x00, 0x01, 0x00, 0x3C, 0x40, 0x03, 0x00, 0x03, 0x02, 0x01, 0x00, 0xF6]

# _open = struct.pack("%dB" % (len(_open)), *_open)
# _close = struct.pack("%dB" % (len(_close)), *_close)

_open = "\x95\x01\x02\x19\xA2\xB1\x00\x02\x83\x00\x00\x00\x3C\x40\x03\x00\x03\x02\x01\x01\xF6"
_close = "\x95\x01\x02\x19\xA2\xB1\x00\x02\x83\x00\x01\x00\x3C\x40\x03\x00\x03\x02\x01\x00\xF6"


def get_response(msg):
    apiUrl = 'http://api.heclouds.com/cmds'
    querystring = {"device_id": "35234481"}
    data = msg

    try:
        headers = {'api-key': API_KEY}
        r = requests.request('POST', apiUrl, params=querystring, data=data, headers=headers).json()
        print (r)
    except Exception, ex:
        print (ex.message)
        return


get_response(_open)