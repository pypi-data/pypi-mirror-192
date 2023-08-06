"""Some test classes
"""
from zope import component
from zope import interface
from zope import schema
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.dublincore.interfaces import IZopeDublinCore

from z3c.configurator import configurator


class ISingleArg(interface.Interface):

    arg = schema.TextLine(title='Some Argument')


class SetTitle(configurator.SchemaConfigurationPluginBase):
    """makes an object implement IFoo"""
    component.adapts(IAttributeAnnotatable)
    schema = ISingleArg

    def __call__(self, data):
        dc = IZopeDublinCore(self.context)
        dc.title = data.get('arg')


class SetDescription(configurator.SchemaConfigurationPluginBase):

    component.adapts(IAttributeAnnotatable)
    schema = ISingleArg

    def __call__(self, data):
        dc = IZopeDublinCore(self.context)
        dc.description = data.get('arg')
