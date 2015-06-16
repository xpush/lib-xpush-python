import collections
import simplejson as json
from socketIO_client import SocketIO, LoggingNamespace
from requests import Session
from connection import Connection

request = Session()

SESSION, CHANNEL = "session", "channel"

class XPush(object):

	hostname = ""
	appId = ""
	userEventNames = {}
	_channels = {}
	Context = None

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
		ch = self._makeChannel(channel, data)
		ch.connect( callback )
		return ""

	def _makeChannel(self, channel, server):
		print( server )
		ch = Connection(self, CHANNEL, server)
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

	def getChannelAsync(self, channel ):
		ch = self.getChannel(channel);
		return ch

	def getChannel(self, channel ):
		print( self._channels )
		return self._channels.get( channel )

	def on_response(*args):
		print('on_response', args)

	def send(self, channel, name, data ):
		ch = self.getChannelAsync(channel)
		ch.send(name,data,self.on_response)