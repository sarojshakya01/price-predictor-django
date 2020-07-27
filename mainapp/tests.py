from .models import *
from django.test import TestCase
from datetime import datetime
from django.utils import timezone

PAGE_FOUND = 200
PAGE_NOT_FOUND = 404
RIDIRECTED = 302


class ViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usercreds = UserCredentials.objects.create(userid=1, username='testuser', password='test123',
                                                       confirm_password='test123')
        cls.usercreds2 = UserCredentials.objects.create(userid=2, username='testuser2', password='test123',
                                                        confirm_password='test123')
        cls.sesson = Sessions.objects.create(userid=1, status=True)
        cls.sesson = Sessions.objects.create(userid=2, status=False)
        cls.userinfo = ClientInformations.objects.create(userid=cls.usercreds, fullname='Test User', address1='Houston', state="TX",
                                                         address2='')
        cls.userinfo2 = ClientInformations.objects.create(userid=cls.usercreds2, fullname='Test User2', address1='Houston', state="NY",
                                                          address2='')
        cls.history = FuelQuotes.objects.create(userid=cls.usercreds,  req_gallons=200, del_address=cls.userinfo.address1,
                                                delivery_date=datetime.today().strftime('%Y-%m-%d'), sugg_price=0, due_amount=0)
        cls.history2 = FuelQuotes.objects.create(userid=cls.usercreds2,  req_gallons=200, del_address=cls.userinfo2.address1,
                                                 delivery_date=datetime.today().strftime('%Y-%m-%d'), sugg_price=0, due_amount=0)
        cls.state = States.objects.create(stateid=1, code="TX", name="Texas")
        cls.state = States.objects.create(stateid=2, code="NY", name="Texas")
        cls.usercreds3 = UserCredentials.objects.create(userid=3, username='testuser3', password='test123',
                                                        confirm_password='test123')

    # app is running
    def test_app_run(self):
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, PAGE_FOUND)

     # login page ok
    def test_login_page(self):
        response = self.client.get('http://127.0.0.1:8000/login')
        self.assertEqual(response.status_code, PAGE_FOUND)

    # register page ok
    def test_register_page(self):
        response = self.client.get('http://127.0.0.1:8000/register')
        self.assertEqual(response.status_code, PAGE_FOUND)

    # create profile page fail
    def test_create_profile_page_get_fail(self):
        response = self.client.get('http://127.0.0.1:8000/create_profile')
        self.assertEqual(response.status_code, RIDIRECTED)

    # create profile page ok
    def test_create_profile_page(self):
        session = self.client.session
        session['username'] = 'testuser'
        session['password'] = 'test123'
        session.save()
        response = self.client.get('http://127.0.0.1:8000/create_profile')
        self.assertEqual(response.status_code, PAGE_FOUND)

    # login with previus session exits
    def test_login(self):
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': 'testuser', 'password': 'test123'})
        self.assertEqual(response.status_code, RIDIRECTED)

    # login with previus session not exit
    def test_login2(self):
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': 'testuser3', 'password': 'test123'})
        self.assertEqual(response.status_code, RIDIRECTED)

    # login with blank username
    def test_login_fail(self):
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': '', 'password': 'test123'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # login with mismatched password
    def test_login_fail2(self):
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': 'testuser', 'password': 'test12a3'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # register with no user
    def test_create_user_fail(self):
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': '', 'password': 'wrong', 'confirm_password': 'wrong'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # register with mismatched password
    def test_create_user_fail2(self):
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': '', 'password': 'wrong', 'confirm_password': 'wrong1'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # register already existed user
    def test_create_userfail3(self):
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': 'testuser', 'password': 'test123', 'confirm_password': 'test123'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # register new user
    def test_create_user(self):
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': 'testuser1', 'password': 'test123', 'confirm_password': 'test123'})
        self.assertEqual(response.status_code, RIDIRECTED)

    # create user with invalid form value
    def test_user_profile_fail(self):
        session = self.client.session
        session['username'] = 'testuser'
        session['password'] = 'test123'
        session.save()
        response = self.client.post(
            'http://127.0.0.1:8000/create_profile', {'fullname': '', 'address1': 'Test Address'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # create user  profile
    # def test_user_profile(self):
    #     session = self.client.session
    #     session['id'] = '1'
    #     session.save()
    #     response = self.client.post(
    #         'http://127.0.0.1:8000/create_profile', {'fullname': 'Test User', 'address_1': 'Test Address', 'address_2': 'TEST', 'city': 'Test City', 'state': 'AB', 'zip': '23232'})
    #     self.assertEqual(response.status_code, RIDIRECTED)

    # redirect to edit profile page
    def test_user_profile_click(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/edit_profile')
        self.assertEqual(response.status_code, PAGE_FOUND)

    # update user profile for logged in user
    def test_user_profile_update(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.post(
            'http://127.0.0.1:8000/create_profile', {'fullname': 'Test UserX', 'address_1': 'Test Address', 'address_2': 'TEST', 'city': 'Test City', 'state': 'TX', 'zip': '23232'})
        self.assertEqual(response.status_code, RIDIRECTED)

    # update user profile for not logged in user
    def test_user_profile_update_Fail(self):

        session = self.client.session
        session['id'] = '2'
        session['username'] = 'testuser'
        session['password'] = 'test123'
        session.save()
        response = self.client.post(
            'http://127.0.0.1:8000/create_profile', {'fullname': 'Test UserX', 'address_1': 'Test Address', 'address_2': 'TEST', 'city': 'Test City', 'state': 'TX', 'zip': '23232'})
        self.assertEqual(response.status_code, RIDIRECTED)

    # user has active session
    def test_getQuote(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, PAGE_FOUND)

    # user does not have active session
    def test_getQuote_fail(self):
        session = self.client.session
        session['id'] = '2'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, RIDIRECTED)

    # not existing user
    def test_getQuote_fail2(self):
        session = self.client.session
        session['id'] = '4'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, RIDIRECTED)

    # not existing session
    def test_getQuote_fail3(self):
        session = self.client.session
        session['id'] = '3'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, RIDIRECTED)

    # not existing session
    def test_getQuote_fail4(self):
        response = self.client.get(
            'http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, RIDIRECTED)

    # invalid quote form
    def test_post_quote_fail(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.post('http://127.0.0.1:8000/quote', {'userid': 1,  'gallonreq': '0', 'deladdress': 'Houston, Texas',
                                                                    'deliverydate': '2020-06-27', 'suggprice': '145.59', 'deuamount': '290000'})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # valid quote form
    def test_post_quote(self):
        # redirect to another page
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.post('http://127.0.0.1:8000/quote', {'userid': 1,  'gallonreq': '200', 'deladdress': 'Houston, Texas',
                                                                    'deliverydate': '2020-06-27', 'suggprice': '145.59', 'deuamount': '290000'})
        self.assertEqual(response.status_code, RIDIRECTED)

    def test_postSuggPrice(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.post(
            'http://127.0.0.1:8000/suggested_price', {'gallon_req': 2000})
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_postSuggPriceFail(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.post(
            'http://127.0.0.1:8000/suggested_price', {'gallon_req': 0})
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_getSuggPriceFail(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/suggested_price', {'gallon_req': 10})
        self.assertEqual(response.status_code, PAGE_FOUND)

    # with valid session
    def test_getHistory(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/history')
        self.assertEqual(response.status_code, PAGE_FOUND)

    # with invalid session
    def test_getHistoryfail(self):
        session = self.client.session
        session['id'] = '2'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/history')
        self.assertEqual(response.status_code, RIDIRECTED)

    # with no session
    def test_getHistoryfail2(self):
        session = self.client.session
        session['id'] = '3'
        session.save()
        response = self.client.get(
            'http://127.0.0.1:8000/history')
        self.assertEqual(response.status_code, RIDIRECTED)

    # with no user
    def test_getHistoryfail3(self):
        response = self.client.get(
            'http://127.0.0.1:8000/history')
        self.assertEqual(response.status_code, RIDIRECTED)

    # logout ok
    def test_logout(self):
        session = self.client.session
        session['id'] = '1'
        session.save()
        response = self.client.get('http://127.0.0.1:8000/logout')
        self.assertEqual(response.status_code, RIDIRECTED)

    # logout fail with no user
    def test_logout_fail(self):
        response = self.client.get('http://127.0.0.1:8000/logout')
        self.assertEqual(response.status_code, RIDIRECTED)

    # logout fail with post request
    def test_logout_fail2(self):
        response = self.client.post('http://127.0.0.1:8000/logout')
        self.assertEqual(response.status_code, RIDIRECTED)

    # random page not found ok
    def test_random_page(self):
        response = self.client.get('http://127.0.0.1:8000/notfound')
        self.assertEqual(response.status_code, PAGE_NOT_FOUND)


class ModelTestCase(TestCase):
    def create_user(self):
        return UserCredentials.objects.create(username="testuser", password="test123", confirm_password="test123")

    def create_state(self):
        return States.objects.create(cide="AB", name="Abibas")

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
