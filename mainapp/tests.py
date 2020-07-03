from django.test import TestCase

PAGE_FOUND = 200
PAGE_NOT_FOUND = 404
FORM_SUBMITTED = 302
FORM_SUBMIT_FAILED = 200


class ViewsTestCase(TestCase):
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

    def test_quote_page(self):
        # quote form page ok
        response = self.client.get('http://127.0.0.1:8000/quote')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_history_page(self):
        # history page ok
        response = self.client.get('http://127.0.0.1:8000/history')
        self.assertEqual(response.status_code, PAGE_FOUND)

    def test_random_page(self):
        # random page not found ok
        response = self.client.get('http://127.0.0.1:8000/notfound')
        self.assertEqual(response.status_code, PAGE_NOT_FOUND)

    def test_post_login(self):
        # redirect to another page
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': 'demouser', 'password': '12345'})
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_post_login_with_wrong_pw(self):
        # should remain in same page for wrong password
        response = self.client.post(
            'http://127.0.0.1:8000/login', {'username': 'demouser', 'password': '12254'})
        self.assertEqual(response.status_code, FORM_SUBMIT_FAILED)

    def test_post_register(self):
        # redirect to another page
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': 'newuser', 'password': '11111', 'confirm_password': '11111'})
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_post_register_with_mismatch_pw(self):
        # should remain in same page for mismatched password
        response = self.client.post(
            'http://127.0.0.1:8000/register', {'username': 'newuser', 'password': '11111', 'confirm_password': '12333'})
        self.assertEqual(response.status_code, FORM_SUBMIT_FAILED)

    def test_post_user_create(self):
        # redirect to another page
        response = self.client.post('http://127.0.0.1:8000/create_profile', {'fullname': 'New User', 'address_1': 'Houston, Texas',
                                                                             'address_2': 'Houston, Texas', 'city': 'Houston', 'state': 'TX', 'zip': '123456'})
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_post_user_create_invalid_fullname(self):
        # should remain in same page for no username
        response = self.client.post('http://127.0.0.1:8000/create_profile', {'fullname': '', 'address_1': 'Houston, Texas',
                                                                             'address_2': 'Houston, Texas', 'city': 'Houston', 'state': 'TX', 'zip': '123456'})
        self.assertEqual(response.status_code, FORM_SUBMIT_FAILED)

    def test_post_user_create_invalid_zipcode(self):
        # should remain in same page for 4 character zip code
        response = self.client.post('http://127.0.0.1:8000/create_profile', {'fullname': 'User Name', 'address_1': 'Houston, Texas',
                                                                             'address_2': 'Houston, Texas', 'city': 'Houston', 'state': 'TX', 'zip': '1234'})
        self.assertEqual(response.status_code, FORM_SUBMIT_FAILED)

    def test_post_quote(self):
        # redirect to another page
        response = self.client.post('http://127.0.0.1:8000/quote', {'gallonreq': '200', 'deladdress': 'Houston, Texas',
                                                                    'deliverydate': '2020-06-27', 'suggprice': '145.59', 'deuamount': '290000'})
        self.assertEqual(response.status_code, FORM_SUBMITTED)

    def test_post_quote_invalid_gallonreq(self):
        # should remain in same page for no gallon request value
        response = self.client.post('http://127.0.0.1:8000/quote', {'gallonreq': '', 'deladdress': 'Houston, Texas',
                                                                    'deliverydate': '2020-06-27', 'suggprice': '145.59', 'deuamount': '290000'})
        self.assertEqual(response.status_code, FORM_SUBMIT_FAILED)
