from socketIO_client import SocketIO, BaseNamespace

class XpushNamespace(BaseNamespace):

	def on_response(self, *args):
		print("on_response", args)

	def on_connect(self):
		print("on connect")

	def on_disconnect(self):
		"""Called after socket.io disconnects.
		You can override this method."""

	def on_event(self, event, *args):
		"""Called after socket.io sends an error packet.
		You can override this method."""
		#print("on event ", event)

	def on_error(self, data):
		print("on error ", data)
		"""Called after socket.io sends an error packet.
		You can override this method."""

class Connection(object):
	def __init__(self, xpush, type, server):

		self._xpush = xpush
		self._type = type
		self._server = server
		self._connected = False
		self._socket = None
		self.channel = None
		self.xpushNamespace = None

		self.info = None
		self.chNm = None

	def connect(self, cb):

		appId = self._xpush.appId
		userId = self._xpush.userId
		deviceId = self._xpush.deviceId
		token = self._xpush.token

		q = {
			"A" : appId,
			"U" : userId, 
			"D" : deviceId,
			"C" : 'zztv',
			"S" : '10' 
		}

		strArr = self._server.get( "url" ).split(":")
		protocol = strArr[0]
		host =  strArr[1].replace( "//", "" )
		port = int( strArr[2] )

		socketIO = SocketIO( host, port, params= q )

		self.xpushNamespace = socketIO.define(XpushNamespace, "/"+self._type)

		#socketIO.emit("aaa", {"xxx": "yyy"})

		self._connected = True
		self._socket = socketIO
		#self._socket.wait()

		cb()

	def send(self, name, data, cb):

		if(self._connected):
			self._socket.emit("send", {"NM": name , "DT": data})
			self._socket.on('message', self.xpushNamespace.on_response)
			self._socket.wait_for_callbacks(seconds=2)
			self._socket.wait()
			print( "123123" )
			cb()
	
	def setServerInfo(self, info, cb):
		url = info.get( "server" ).get( "url" )
		self._server = { "serverUrl" : url}
		self.chNm = info.get( "channel" )