# -*- coding: utf-8 -*-
from ..settings import ISettingsSchema
from datetime import datetime
from datetime import timedelta
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from rer.newsletter import logger
from rer.newsletter.utils import storage
from zope.interface import alsoProvides


class DeleteExpiredUsersView(BrowserView):
    """ Delete expired users from channels """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update_annotations(self, channel):
        expired_date = datetime.now()
        expired_time_token = api.portal.get_registry_record(
            'expired_time_token', ISettingsSchema)

        annotations = storage(channel.getObject())
        for val in annotations.keys():
            creation_date = datetime.strptime(
                annotations[val]['creation_date'],
                '%d/%m/%Y %H:%M:%S')
            if creation_date + timedelta(hours=expired_time_token) < expired_date and not annotations[val]['is_active']:  # noqa
                del annotations[val]

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        logger.info(u'START:Remove expired user from channels')
        channels_brain = api.content.find(
            context=api.portal.get(),
            portal_type='Channel'
        )
        map(lambda x: self.update_annotations(x), channels_brain)
        logger.info(u'DONE:Remove expired user from channels')
        return True
