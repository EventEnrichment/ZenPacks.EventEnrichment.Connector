import logging
log = logging.getLogger('zen.ZenPacks.EE.Connector')

import json
import datetime
from urlparse import urlparse
import urllib2

from zope.interface import implements
from zenoss.protocols.protobufs.zep_pb2 import SEVERITY_CLEAR, SEVERITY_DEBUG, SEVERITY_INFO, SEVERITY_WARNING, SEVERITY_ERROR, SEVERITY_CRITICAL

from Products.ZenModel.actions import IActionBase, ActionExecutionException
from Products.ZenModel.interfaces import IAction
from Products.Zuul.interfaces.actions import ICommandActionContentInfo
from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenModel.ZVersion import VERSION as ZENOSS_VERSION

from ZenPacks.EE.Connector.router import EE_API_KEY

EE_SEVERITY_INFO = 'info'
EE_SEVERITY_WARNING = 'warning'
EE_SEVERITY_ERROR = 'error'
EE_SEVERITY_CRITICAL = 'critical'

SEVERITY_MAP = { 
    SEVERITY_INFO: EE_SEVERITY_INFO,
    SEVERITY_WARNING: EE_SEVERITY_WARNING,
    SEVERITY_ERROR: EE_SEVERITY_ERROR,
    SEVERITY_CRITICAL: EE_SEVERITY_CRITICAL
    }

# for development in lab 
#ESRV_PROTO_HOST_PORT = 'http://172.16.0.199:3000'

# this will become our public event API endpoint
ESRV_PROTO_HOST_PORT = 'http://eep.eventenrichment.com'

EVENT_URL = ESRV_PROTO_HOST_PORT + '/api/v1/event'
CLEAR_URL = ESRV_PROTO_HOST_PORT + '/api/v1/clear'
                 
class ConnectorAction(IActionBase):
    implements(IAction)

    id = 'ee_connector'
    name = 'EE Connector'
    actionContentInfo = ICommandActionContentInfo

    def updateContent(self, content=None, data=None):
        log.debug("%s updateContent: content=%s data=%s", self, content, data)
        content.update(data)

    def execute(self, notification, signal):
        log.debug("%s execute: notification=%s signal=%s", self, notification, signal)

        # read api_key from storage
        api_key = getattr(self.dmd, EE_API_KEY, None)
        if api_key == None:
            log.error("EE Connector attribute %s not configured" % EE_API_KEY)
            return

        event = signal.event
        occurrence = event.occurrence[0]
        actor = occurrence.actor

        # disregard SEVERITY_DEBUG
        if occurrence.severity == SEVERITY_DEBUG:
            log.debug("%s execute: disregarding event %s with severity %d", self, event.uuid, occurrence.severity)
            return

        if signal.clear:
            url = CLEAR_URL
            pbody = {
                'local_instance_id': event.uuid,
                'source_location': actor.element_identifier
                }
            packet = { 'api_token': api_key, 'clear': pbody }
            
        else:
            url = EVENT_URL
            pbody = { 
                'local_instance_id': event.uuid,
                'creation_time': self._epochMsToIso8601(event.first_seen_time),
                'last_time': self._epochMsToIso8601(event.last_seen_time),
                'severity': SEVERITY_MAP[occurrence.severity],
                'msg': occurrence.message,
                'event_class': occurrence.event_class,
                'source_location': actor.element_identifier,
                'source_component': actor.element_sub_identifier,
                'reporter_location': urlparse(self.options['zopeurl']).hostname,
                'reporter_component': 'Zenoss_' + ZENOSS_VERSION,
                'repeat_count': event.count
                }

            packet = { 'api_token': api_key, 'event': pbody }
        
        request_body = json.dumps(packet)

        # post request to esrv
        headers = {
            'Accept' : 'application/json', 
            'Content-type' : 'application/json' 
            }
        req = urllib2.Request(url, request_body, headers)
        try:
            response = urllib2.urlopen(req, None, 60)
        except urllib2.URLError as e:
            ### this error logging will expose api_key - use pbody instead?
            if hasattr(e, 'reason'):
                raise ActionExecutionException("Error posting request %s to %s - reason: %s" % (request_body, url, e.reason))
            elif hasattr(e, 'code'):
                self._parseErrMsgs(e)
                raise ActionExecutionException("Error posting request %s to %s - HTTP code: %d, reason: %s" % (request_body, url, e.code, e.msg))
            else:
                raise ActionExecutionException("Error posting request %s to %s - URLError: %s" % (request_body, url, e))

        log.info("response.code: %d", response.getcode())
        log.info("response.headers: %s", response.info())
        log.info("response.body: %s", response.read())
        
        response.close()

    def setupAction(self, dmd):
        log.info("%s setupAction: dmd=%s", self, dmd)
        self.guidManager = GUIDManager(dmd)
        self.dmd = dmd

    def _epochMsToIso8601(self, epochMs):    
        dt = datetime.datetime.fromtimestamp(epochMs / 1000)
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')        

    # if HTTP 400 or 422, parse response body json for error messages
    def _parseErrMsgs(self, ue):
        if ue.code == 400 or ue.code == 422:
            h = json.loads(ue.read())
            log.error("Esrv rejected event with status %d - error messages:", ue.code)
            for emsg in h['messages']:
                log.error(emsg)

                
        
                    
