"""Archetypes widgets have a .visible property.

By default it may be True or False, or it may contain a dictionary:

            visible={'edit': 'visible',
                     'view': 'visible'}

Values may be 'visible', 'invisible', or 'hidden' depending on how we want
the widget to display in different modes.

The adapters in WidgetVisibility extend the possibilities of this variable.
To define rules for showing/hiding fields at runtime, this is the best way.

For simpler field visibility configuration examine extenders/analysisrequest.py
where the widget.visible flag is used to control adapters in bika.lims.
"""
from zope.interface import implements

from bika.lims.interfaces import IATWidgetVisibility
from bika.sanbi.interfaces import IAliquot, IBiospecimen


class CustomFieldWidgetVisibility(object):
    """Forces a set of AnalysisRequest fields to be invisible depending on
    some arbitrary condition.
    """
    implements(IATWidgetVisibility)

    def __init__(self, context):
        self.context = context
        self.sort = 10
        self.hidden_fields = ['AdHoc', 'Composite', 'InvoiceExclude']
        self.random = 4  # fair dice roll

    def __call__(self, context, mode, field, default):
        state = default if default else 'hidden'
        fieldName = field.getName()
        if not self.context.getClient():
            if fieldName in []:
                return 'invisible'
        return state

class SampleFieldWidgetVisibility(object):
    """Forces a set of Sample fields to be invisible depending on
    if context implement IBiospecimen or IAliquot
    """
    implements(IATWidgetVisibility)

    def __init__(self, context):
        self.context = context
        self.sort = 10
        self.random = 4
        if IAliquot.providedBy(context):
            self.hidden_fields = ['Kit', 'SubjectID',
                                  'Barcode', 'Sampling Date',
                                  'ScheduledSamplingSampler',
                                  'PreparationWorkflow',
                                  'SamplePoint', 'Sampler']

        if IBiospecimen.providedBy(context):
            self.hidden_fields = ['Sampling Date',
                                  'LinkedSample',
                                  'ScheduledSamplingSampler',
                                  'PreparationWorkflow',
                                  'SamplePoint', 'Sampler']

    def __call__(self, context, mode, field, default):
        state = default if default else 'hidden'
        field_name = field.getName()
        if field_name in self.hidden_fields and mode == 'header_table':
            field.required = False
            return 'invisible'

        return state