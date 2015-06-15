import simplejson as json
from xpush import Connection, XPush

def on_response(*args):
	print('on_response', args)

xpush = XPush( 'http://localhost:8000', 'demo' )
channel = 'channel01'

response = xpush.rest( xpush.Context.get( 'NODE' )+'/'+xpush.appId+'/'+channel , 'GET', {}, {} )
res = json.loads( response )
url = res.get( "result" ).get( "server" ).get( "url" )

ch = Connection( xpush, 'channel', url )
ch.connect( on_response )
ch.send( "message", { "AA":"BB", "CC":"DD" }, on_response )