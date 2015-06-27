import collections
import simplejson as json
from socketIO_client import SocketIO, LoggingNamespace
from requests import Session
from connection import Connection

request = Session()

TYPE_SESSION, TYPE_CHANNEL = "session", "channel"

class XPush(object):

	hostname = ""
	appId = ""
	userEventNames = {}
	_channels = {}
	Context = None
	_sessionConnection = None

	def __init__(self, host, appId, eventHandler=None, autoInitFlag=True):
		if host is None:
			return 'params(1) must have hostname'
		if appId is None:
			return 'params(2) must have appId'

		self.hostname = host #applicationKey
		self.appId = appId	#applicationKey

		self.userId = "someone"
		self.deviceId = "WEB"
		self.token = ""
		self.info = None

		self.Context = {
      "SIGNUP" : '/user/register',
      "LOGIN" : '/auth',
      "Channel" : '/channel',
      "Signout" : '/signout',
      "Message" : '/msg',
      "NODE" : '/node'
    }

	def createSimpleChannel(self, channel, userObj, callback):
		data = self._getChannelInfo(channel)
		ch = self._makeChannel(channel, data, True)
		ch.connect( callback )

	def _makeChannel(self, channel, server, channelOnly=False):
		ch = Connection(self, TYPE_CHANNEL, server, channel, channelOnly)
		if channel :
			ch.channel = channel
			self._channels[channel] = ch
		return ch

	def _getChannelInfo(self, channel):
		response = self.rest( self.Context.get('NODE')+'/'+self.appId+'/'+channel , 'GET', {}, {} )
		res = json.loads( response )
		return res.get( "result" ).get( "server" )

	def rest(self, context, method, data, headers ):
		if method == 'GET' :
			url = self.hostname+context
			response = request.get( url )
			return response.text

		else :
			url = self.hostname+context
			response = request.post(
				url=url,
				data=data,
				headers=headers
			)
			return response.text

	def getChannelAsync(self, channel):
		ch = self.getChannel(channel);
		if ch is None :
			self._channels[channel] = ch

			serverInfo = self._getChannelInfo(channel)
			ch = self._makeChannel(channel, serverInfo)

			if( serverInfo ) :
				ch.setServerInfo(serverInfo)

		return ch

	def getChannel(self, channel ):
		return self._channels.get( channel )

	def on_response(*args):
		print('on_response', args)

	def send(self, channel, name, data ):
		ch = self.getChannelAsync(channel)
		ch.send(name,data,self.on_response)

	def joinChannel(self,channel,param,cb):
		ch = self.getChannelAsync(channel)
		ch.joinChannel( param, cb )

	def login(self,userId, password, deviceId, cb):
		self.userId = userId
		if deviceId is None :
			deviceId = 'WEB'

		self.deviceId = deviceId

		sendData = {"A": self.appId, "U": userId, "PW": password, "D": deviceId}
		response = self.rest( self.Context.get('LOGIN'), 'POST', sendData, {} )
		res = json.loads( response )

		url = res.get( "result" ).get( "serverUrl" )
		name = res.get( "result" ).get( "server" )
		self.token = res.get( "result" ).get( "token" )

		serverInfo = {
			"url" : url,
			"name" : name
		}

		if res.get( "status" ) == 'ok' :
			self._sessionConnection = Connection(self, TYPE_SESSION, serverInfo, False);
			self._sessionConnection.connect( self._sessionConnectCallback );

			print( res )

	def signup(self, userId, password, deviceId, cb):
		sendData = {"A": self.appId, "U": userId, "PW": password, "D": deviceId}
		response = self.rest( self.Context.get('SIGNUP') , 'POST', sendData, {} )
		res = json.loads( response )

	def _initSessionSocket(self, socket):
		print( 'init session' )

	def _sessionConnectCallback(self) :
		self._initSessionSocket(self._sessionConnection._socket)