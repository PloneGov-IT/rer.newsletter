# call utility
from zope.component import getUtility
from rer.newsletter.utility.newsletter import INewsletterUtility
from rer.newsletter.utility.newsletter import UNHANDLED, OK
from rer.newsletter import logger

from zope.interface import Interface, implements
from Products.Five import BrowserView

# template manage
from Products.CMFPlone.resources import add_bundle_on_request

# file
import csv
import StringIO

import json
import ast


class IManageUsers(Interface):
    pass


class ManageUsers(BrowserView):
    implements(IManageUsers)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        add_bundle_on_request(self.request, 'datatables')

    def deleteUserFromNewsletter(self):

        try:
            email = self.request['email']
            newsletter = self.context.idNewsletter

            api_newsletter = getUtility(INewsletterUtility)
            status = api_newsletter.deleteUser(newsletter, email)
        except:
            logger.exception(
                'unhandled error subscribing %s %s',
                newsletter,
                email
            )
            self.errors = u"Problem with subscribe"
            status = UNHANDLED

        response = {}
        if status == OK:
            response['ok'] = True
        else:
            response['ok'] = False

        return json.dumps(response)

    def exportUsersListAsFile(self):

        try:
            newsletter = self.context.idNewsletter

            api_newsletter = getUtility(INewsletterUtility)
            userList, status = api_newsletter.exportUsersList(newsletter)
        except:
            logger.exception(
                'unhandled error on export of user %s',
                newsletter
            )
            self.errors = u"Problem with export"
            status = UNHANDLED

        if status == OK:
            # predisporre download del file
            data = StringIO.StringIO()
            fieldnames = ['id', 'Emails']
            writer = csv.DictWriter(data, fieldnames=fieldnames)

            writer.writeheader()
            userList = ast.literal_eval(userList)
            for user in userList:
                writer.writerow(user)

            filename = "%s-user-list.csv" % self.context.title

            self.request.response.setHeader('Content-Type', 'text/csv')
            self.request.response.setHeader(
                'Content-Disposition',
                'attachment; filename="%s"' % filename
            )

            return data.getvalue()

    def exportUsersListAsJson(self):

        try:
            newsletter = self.context.idNewsletter

            api_newsletter = getUtility(INewsletterUtility)
            userList, status = api_newsletter.exportUsersList(newsletter)
        except:
            logger.exception(
                'unhandled error on export of user %s',
                newsletter
            )
            self.errors = u"Problem with export"
            status = UNHANDLED

        if status == OK:
            return userList
