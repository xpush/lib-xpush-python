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

TYPE_SESSION, TYPE_CHANNEL = "session", "channel"

class Connection(object):
	def __init__(self, xpush, type, server, chNm, channelOnly=False):

		self._xpush = xpush
		self._type = type

		if(self._type == TYPE_SESSION):
			self.chNm = TYPE_SESSION
		else :
			self.chNm = chNm

		self._server = server
		self._connected = False
		self._socket = None
		self.channel = None
		self.xpushNamespace = None

		self.info = None

		self._channelOnly = channelOnly

	def connect(self, cb):

		appId = self._xpush.appId
		userId = self._xpush.userId
		deviceId = self._xpush.deviceId
		token = self._xpush.token
		serverName = self._server.get( "name" )

		q = {
			"A" : appId,
			"U" : userId, 
			"D" : deviceId,
			"C" : self.chNm,
			"S" : serverName
		}

		if self._channelOnly == True :
			q["MD"] = "CHANNEL_ONLY";

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
	
	def setServerInfo(self, serverInfo, cb=None):
		url = serverInfo.get( "url" )
		self._server = { "serverUrl" : url}
		self.chNm = serverInfo.get( "channel" )

	def disconnect(self) :
		self._socket.disconnect()

	def send(self, name, data, cb):

		if(self._connected):
			self._socket.emit("send", {"NM": name , "DT": data})
			self._socket.on('message', self.xpushNamespace.on_response)
			self._socket.wait_for_callbacks(seconds=2)
			#self._socket.wait()
			cb()

	def joinChannel(self, param, cb) :
		if(self._connected):
			self._socket.emit('join', param, cb)
