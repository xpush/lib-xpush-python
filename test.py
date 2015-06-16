import simplejson as json
from xpush import Connection, XPush

def on_response(*args):
	print('on_response', args)

xpush = XPush( 'http://localhost:8000', 'P-00001' )
channel = 'zztv'

xpush.createSimpleChannel( channel, {}, on_response )

xpush.send( channel, "message", { "AA":"BB", "CC":"DD" } )