import collections
from socketIO_client import SocketIO, LoggingNamespace
from requests import Session

session = Session()

SESSION, CHANNEL = "session", "channel"

class XPush(object):

	hostname = ""
	appId = ""
	userEventNames = {}
	channels = {}

	def __init__(self, host, appId, eventHandler=None, autoInitFlag=True):
		if host is None:
			return 'params(1) must have hostname'
		if appId is None:
			return 'params(2) must have appId'

		self.hostname = host #applicationKey
		self.appId = appId	#applicationKey

		self.userId = ""
		self.deviceId = ""
		self.token = ""

		self.Context = {
      "SIGNUP" : '/user/register',
      "LOGIN" : '/auth',
      "Channel" : '/channel',
      "Signout" : '/signout',
      "Message" : '/msg',
      "NODE" : '/node'
    }

	def createSimpleChannel(self, channel, userObj, callback):
		ch = _makeChannel(channel)
		data = self._getChannelInfo(channel)

		return ""

	@classmethod
	def _makeChannel(channel):
		ch = Connection(self,CHANNEL)
		if channel :
			ch.channel = channel
			self._channels[channel] = ch
		return ch

	@classmethod
	def _getChannelInfo(channel, cb):
		response = self.rest( self.Context.get('NODE')+'/'+self.appId+'/'+channel , 'GET', {}, {} )
		return response

	def rest(self, context, method, data, headers ):
		if method == 'GET' :
			url = self.hostname+context
			response = session.get( url )
			return response.text

		else :
			url = self.hostname+context
			response = session.post(
				url=url,
				data=data,
				headers=headers
			)
			return response.text