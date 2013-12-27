import logging
log = logging.getLogger('zen.ZenPacks.EE.Connector')

from Products.ZenUtils.Ext import DirectResponse
from Products.ZenUtils.extdirect.zope.router import ZopeDirectRouter
from Products.ZenWidgets.messaging import MessageSender

EE_API_KEY = 'ee_api_key'

class EeRouter(ZopeDirectRouter):
    def loadSettings(self, load=True):
        dmd = self.context

        log.info("EeRouter loadSettings")

        if hasattr(dmd, EE_API_KEY):
            h = { EE_API_KEY: dmd.ee_api_key }
            return DirectResponse(data = h)
        else:
            return DirectResponse(None)

    def submitSettings(self, ee_api_key=None):
        log.info("EeRouter submitSettings")
        dmd = self.context
        dmd.ee_api_key = ee_api_key
        
        # flash msg and redirect to reload page
        MessageSender(dmd).sendToBrowser('info', 'EE Api Key saved')
        redir_url = self.request['SERVER_URL'] + '/zport/dmd/ee'
        self.request.response.redirect(redir_url)


