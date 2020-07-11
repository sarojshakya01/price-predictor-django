from django.test import TestCase
from datetime import datetime
from .models import *

PAGE_FOUND = 200
PAGE_NOT_FOUND = 404
FORM_SUBMITTED = 302
FORM_SUBMIT_FAILED = 200


class ViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usercreds = UserCredentials.objects.create(userid=1, username='testuser', password='test123',
                                                       confirm_password='test123')
        cls.sesson = Sessions.objects.create(userid=1, status=True)
        cls.userinfo = ClientInformations.objects.create(userid=cls.usercreds, fullname='Test User', address1='Houston',
                                                         address2='')
        cls.history = FuelQuotes.objects.create(userid=cls.usercreds,  req_gallons=200, del_address=cls.userinfo.address1,
                                                delivery_date=datetime.today().strftime('%Y-%m-%d'), sugg_price=0, due_amount=0)

    def test_app_run(self):
        # app is running
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_login_page(self):
        # login page ok
        response = self.client.get('http://127.0.0.1:8000/login')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_register_page(self):
        # register page ok
        response = self.client.get('http://127.0.0.1:8000/register')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_create_profile_page(self):
        # create profile page ok
        response = self.client.get('http://127.0.0.1:8000/create_profile')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_login(self):
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': 'testuser', 'password': 'test123'})
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_login_fail(self):
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': '', 'password': 'test123'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_login_fail2(self):
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': 'testuser', 'password': 'test12a3'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_create_user_fail(self):
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': '', 'password': 'wrong', 'confirm_password': 'wrong'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_create_user(self):
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': 'newuser', 'password': '12345', 'confirm_password': '12345'})
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_user_profile_fail(self):
        session = self.client.session
        session['username'] = 'testuser'
        session['password'] = 'test123'
        session.save()
        response = self.client.post(
            'http://127.0.0.1:8000/create_profile', {'fullname': '', 'address1': 'Test Address'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # def test_user_profile(self):
    #     session = self.client.session
    #     session['id'] = '1'
    #     session.save()
    #     response = self.client.post(
    #         'http://127.0.0.1:8000/create_profile?id=1', {'fullname': 'Test User', 'address_1': 'Test Address', 'address_2': 'TEST', 'city': 'Test City', 'state': 'AB', 'zip': '23232'})
    #     self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_getQuote(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_getQuote_fail(self):
        session = self.client.session
        session['id'] = '2'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_getHistoy(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/history')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_getHistoyfail(self):
        session = self.client.session
        session['id'] = '2'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/history')
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_logout(self):
        # logout ok
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get('http://127.0.0.1:8000/logout')
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_random_page(self):
        # random page not found ok
        response = self.client.get('http://127.0.0.1:8000/notfound')
        self.assertEqual(response.status_code, PAGE_NOT_FOUND)

    def test_post_quote_fail(self):
        # redirect to another page
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.post('http://127.0.0.1:8000/quote', {'userid': 1,  'gallonreq': '0', 'deladdress': 'Houston, Texas',
                                                                    'deliverydate': '2020-06-27', 'suggprice': '145.59', 'deuamount': '290000'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_post_quote(self):
        # redirect to another page
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.post('http://127.0.0.1:8000/quote', {'userid': 1,  'gallonreq': '200', 'deladdress': 'Houston, Texas',
                                                                    'deliverydate': '2020-06-27', 'suggprice': '145.59', 'deuamount': '290000'})
        self.assertEqual(response.status_code, FORM_SUBMITTED)


class ModelTestCase(TestCase):
    def create_user(self):
        return UserCredentials.objects.create(username="testuser", password="test123", confirm_password="test123")

    def create_userinfo(self):
        user = self.create_user()
        return ClientInformations.objects.create(userid=user, fullname="Test User", address1="Test Address", city="Test City", state="AB", zipcode="223232")

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, UserCredentials))
        self.assertEqual(user.__unicode__(), user.username)

    def test_profile_creation(self):
        user = self.create_userinfo()
        self.assertTrue(isinstance(user, ClientInformations))
        self.assertEqual(user.__unicode__(), user.fullname)
