from Products.CMFCore.utils import getToolByName
from bika.sanbi import bikaMessageFactory as _
from zope.interface.declarations import implements
from bika.sanbi.permissions import *
from bika.lims.browser.bika_listing import BikaListingView

from plone.app.layout.globals.interfaces import IViewView
from plone.app.content.browser.interfaces import IFolderContentsView

class PackagesView(BikaListingView):
    implements(IFolderContentsView, IViewView)
        
    def __init__(self, context, request):
        super(PackagesView, self).__init__(context, request)
        self.contentFilter = {'portal_type': 'SupplyEx',
                              'sort_on': 'sortable_title'}
        self.context_actions = {}
        self.title = self.context.translate(_("Packages"))
        self.icon = self.portal_url + "/++resource++bika.lims.images/container_big.png"
        self.description = ""
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = False
        self.pagesize = 50

        self.columns = {
            'kitID': {'title': _('Kit ID'),
                      'index': 'sortable_title',
                      'toggle': True},
            'kitTemplate': {'title': _('Kit template'),
                       'toggle': True},
            'quantity': {'title': _('Quantity'),
                       'toggle': True},
        }

        self.review_states = [
            {'id':'default',
             'title': _('Valid'),
             'contentFilter': {'review_state': 'valid'},
             'transitions': [{'id':'discard'}, ],
             'columns': ['kitID',
                         'kitTemplate',
                         'quantity']},
        ]

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission(AddKitAssembly, self.context):
            self.context_actions[_('Add')] = {
                'url': 'createObject?type_name=SupplyEx',
                'icon': '++resource++bika.lims.images/add.png'
            }
        if mtool.checkPermission(ManagePackages, self.context):
            self.review_states[0]['transitions'].append({'id':'deactivate'})
            self.review_states.append(
                {'id':'discarded',
                 'title': _('Discarded'),
                 'contentFilter': {'review_state': 'discarded'},
                 'transitions': [{'id':'keep'}, ],
                 'columns': ['kitID',
                             'kitTemplate',
                             'quantity']})
            self.review_states.append(
                {'id':'all',
                 'title': _('All'),
                 'contentFilter':{},
                 'columns': ['kitID',
                             'kitTemplate',
                             'quantity']})
            stat = self.request.get("%s_review_state"%self.form_id, 'default')
            self.show_select_column = stat != 'all'
        return super(PackagesView, self).__call__()

    def folderitems(self):
        items = super(PackagesView, self).folderitems()
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj']
            items[x]['kitTemplate'] = obj.getKitTemplateTitle()
            items[x]['replace']['kitID'] = "<a href='%s'>%s</a>" % \
                (items[x]['url'], obj.getKitId())

        return items
