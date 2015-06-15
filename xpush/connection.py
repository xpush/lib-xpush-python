from socketIO_client import SocketIO, BaseNamespace

class XpushNamespace(BaseNamespace):

	def on_response(self, *args):
		print("on_response", args)

	def on_connect(self):
		print(self)

class Connection(object):
	def __init__(self, xpush, type, server):

		self._xpush = xpush
		self._type = type
		self._server = server
		self._connected = False
		self._socket = None

	def connect(self, cb):

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

		#xpush_namespace = socketIO.define(XpushNamespace, "/"+self._type)

		#socketIO.on_connect("connect", xpush_namespace.on_response )
		#socketIO.emit("aaa", {"xxx": "yyy"})

		#print( xpush_namespace )

		self._connected = True
		self._socket = socketIO
		cb()

	def send(self, name, data, cb):

		if(self._connected):
			self._socket.emit("send", {"NM": name , "DT": data})
			cb()