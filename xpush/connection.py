from socketIO_client import SocketIO, BaseNamespace

class XpushNamespace(BaseNamespace):

	def on_aaa_response(self, *args):
		print('on_aaa_response', args)

class Connection(object):
	def __init__(self, xpush, type, server):

		self._xpush = xpush
		self._type = type
		self._server = server

	def connect( self, cb ):

		print( 'appId : ', self._xpush.appId )

		appId = self._xpush.appId
		userId = self._xpush.userId
		deviceId = self._xpush.deviceId
		token = self._xpush.token

		q = {
			"A" : appId,
			"U" : userId, 
			"D" : deviceId,
			"TK" : token
		}

		strArr = self._server.split(":")
		protocol = strArr[0]
		host =  strArr[1].replace( "//", "" )
		port = int( strArr[2] )

		socketIO = SocketIO( host, port, params= q )
		#xpush_namespace = socketIO.define(XpushNamespace, '/'+self._type)
		#socketIO.on('connect', xpush_namespace.on_aaa_response )
		#socketIO.emit('aaa', {'xxx': 'yyy'})
		#cb()