import Globals

from Products.ZenModel.ZenossSecurity import ZEN_MANAGE_DMD
from Products.ZenModel.DataRoot import DataRoot
from Products.ZenModel.UserSettings import UserSettingsManager
from Products.ZenModel.ZenossInfo import ZenossInfo
from Products.ZenModel.ZenPackManager import ZenPackManager
from Products.ZenUtils.Utils import monkeypatch, unused
unused(Globals)

# init / monkeypatch some stuff - thanks to 
# https://github.com/cluther/ZenPacks.cluther.PagerDuty
# for showing the way

EEP = 'eep'

for klass in (DataRoot, UserSettingsManager, ZenossInfo, ZenPackManager):
    action = EEP
    if klass == ZenPackManager:
        action = '../%s' % action

    fti = klass.factory_type_information[0]
    fti['actions'] = fti['actions'] + ({
        'id': EEP,
        'name': 'EEP',
        'action': action,
        'permissions': (ZEN_MANAGE_DMD,)
    },)


@monkeypatch('Products.ZenUI3.navigation.menuitem.PrimaryNavigationMenuItem')
def update(self):
    '''
    Update subviews for this PrimaryNavigationMenuItem.

    Post-processes default behavior to add our subview. This allows the
    secondary navigation bar to be rendered properly when the user is
    looking at the EEP settings screen.
    '''
    # original gets injected into locals by monkeypatch decorator.
    original(self)

    if '/zport/dmd/dataRootManage' in self.subviews:
        self.subviews.append('/zport/dmd/%s' % EEP)


@monkeypatch('Products.Zuul.facades.triggersfacade.TriggersFacade')
def createNotification(self, id, action, *args, **kwargs):
    '''
    Return a notification given id, action and other arguments.

    Post-processes default behavior to set different default
    notification options depending on action.
    '''

    # original gets injected into locals by monkeypatch decorator.
    notification = original(self, id, action, *args, **kwargs)

    if notification.action == 'ee_connector':
        notification.send_clear = True
        notification.repeat_seconds = 60
        notification.send_initial_occurrence = False

    return notification
