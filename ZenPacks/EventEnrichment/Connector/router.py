import logging
log = logging.getLogger('zen.ZenPacks.EventEnrichment.Connector')

from Products.ZenUtils.Ext import DirectResponse
from Products.ZenUtils.extdirect.zope.router import ZopeDirectRouter
from Products.ZenWidgets.messaging import MessageSender

EEP_API_KEY = 'eep_api_key'

class EepRouter(ZopeDirectRouter):
    def loadSettings(self, load=True):
        dmd = self.context

        log.info("EepRouter loadSettings")

        if hasattr(dmd, EEP_API_KEY):
            h = { EEP_API_KEY: dmd.eep_api_key }
            return DirectResponse(data = h)
        else:
            return DirectResponse(None)

    def submitSettings(self, eep_api_key=None):
        log.info("EepRouter submitSettings")
        dmd = self.context
        dmd.eep_api_key = eep_api_key
        
        # flash msg and redirect to reload page
        MessageSender(dmd).sendToBrowser('info', 'EEP Api Token saved')
        redir_url = self.request['SERVER_URL'] + '/zport/dmd/eep'
        self.request.response.redirect(redir_url)


