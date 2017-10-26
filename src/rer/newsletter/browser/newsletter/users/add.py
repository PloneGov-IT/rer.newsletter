# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.interface import Interface
from zope import schema
from z3c.form import button, form, field

from rer.newsletter import newsletterMessageFactory as _
from rer.newsletter import logger
from rer.newsletter.utility.newsletter import INewsletterUtility
from rer.newsletter.utility.newsletter import SUBSCRIBED
from rer.newsletter.utility.newsletter import UNHANDLED

# messaggi standard della form di dexterity
from Products.statusmessages.interfaces import IStatusMessage
from plone.dexterity.i18n import MessageFactory as dmf

# constraint
import re


def mailValidation(mail):
    # valido la mail
    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        mail
    )
    if match is None:
        return False

    return True


class IAddForm(Interface):
    ''' define field for add user to newsletter '''

    email = schema.TextLine(
        title=u"add user",
        description=u"mail for add user to newsletter",
        required=True,
        constraint=mailValidation
    )


class AddForm(form.Form):

    ignoreContext = True
    fields = field.Fields(IAddForm)

    @button.buttonAndHandler(u"add")
    def handleSave(self, action):
        status = UNHANDLED
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        try:

            # TODO
            # questo valore va preso dal contesto in cui mi trovo....
            newsletter = self.context.id_newsletter
            mail = data['email']

            api_newsletter = getUtility(INewsletterUtility)
            status = api_newsletter.addUser(newsletter, mail)
        except:
            logger.exception(
                'unhandled error adding %s %s',
                newsletter,
                mail
            )
            self.errors = u"Problem with add user"

        if status == SUBSCRIBED:
            self.status = u"user added!"
            IStatusMessage(self.request).addStatusMessage(
                dmf(self.status), "info")
            return
        else:
            if 'errors' not in self.__dict__.keys():
                self.errors = u"Ouch .... {}".format(status)

            IStatusMessage(self.request).addStatusMessage(
                dmf(self.errors), "error")
            return
