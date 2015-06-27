import simplejson as json
from xpush import Connection, XPush

def on_response(*args):
	print('on_response', args)

xpush = XPush( 'http://localhost:8000', 'P-00001' )
channel = 'zztv'

#signup test
xpush.signup( 'user04', 'passwd04', 'WEB', on_response )

#login test
xpush.login( 'user04', 'passwd04', 'WEB', on_response )

xpush.createSimpleChannel( channel, {}, on_response )
xpush.joinChannel( channel, {'U':['notdol']}, on_response )
xpush.send( channel, "message", { "AA":"BB", "CC":"DD" } )