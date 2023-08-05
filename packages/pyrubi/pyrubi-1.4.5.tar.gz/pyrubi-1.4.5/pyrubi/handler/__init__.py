from websocket import create_connection as cc
from json import dumps, loads
from ..servers import get_server
from ..cryption import cryption

class handler:

    def __init__(self, auth):
        self.server = get_server('socket')
        self.crypto = cryption(auth)
        self.auth = auth
        del auth

    def hand_shake(self):
        print('connecting to the web socket...')
        ws = cc(self.server)
        ws.send(
            dumps(
                {
                    'api_version': '5',
                    'auth': self.auth,
                    'method': 'handShake'
                }
            )
        )
        if loads(ws.recv())['status'] == 'OK':
            print('connected')
            while True:
                try:
                    recv = loads(ws.recv())
                    if recv['type'] == 'messenger':
                        yield loads(self.crypto.decrypt(recv['data_enc']))
                    else:
                        continue
                except:
                    del ws
                    ws = cc(self.server)
                    ws.send(
                        dumps(
                            {
                                'api_version': '5',
                                'auth': self.auth,
                                'method': 'handShake'
                            }
                        )
                    )
                    continue