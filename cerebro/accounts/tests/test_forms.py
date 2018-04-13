from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client


class SignUpTest(TestCase):

    def __init__(self):
        client = Client()

    def testCreateUser(self, username='test', password='testerGG'):
        '''
        test the creation of a user, duplicate user, and a user with bad credentials
        :param username:
        :param password:
        :return:
        '''
        # test creating a single user
        user = User.objects.create_user(username, password=password)
        user.is_authenticated = True
        user.save()

        # test creating a duplicate user
        userB = User.objects.create_user(username, password=password)
        userB.is_authenticated = True
        self.assertFormError(userB.save())

        # test creating user with bad credentials
        try:
            userC = User.objects.create_user('العَرَبِيَّ', password=password)
            self.assertFormError(userC.save())
            userD = User.objects.create_user(username, password='العَرَبِيَّ')
            self.assertFormError(userD.save())
        except Exception as e:
            print("cannot use foreign langauge %s" % e)

    def testUserLogin(self):
        """
        test for the ability of a regular user to login
        :return:
        """
        username = 'testerAA'
        password = 'testerAA'
        self.testCreateUser(username, password)

        # test incorrect login
        self.client.login('testerAA', 'testerAB')
        self.client.login('testerAB', 'testerAA')
        # test real login
        self.client.login(username, password)

    def testAdminLogin(self):
        """
        test for the ability of an admin user to login
        :return:
        """
        username = 'adminTester'
        password = 'adminTester'
        adminUser = User.objects.create_user(username, password)
        adminUser.is_superuser = True
        adminUser.save()
        self.client.login(username, password)
