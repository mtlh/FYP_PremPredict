from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class LoginGET(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Login"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("Login"))
        self.assertTemplateUsed(response, "login.html")

    def test_template_content(self):
        response = self.client.get(reverse("Login"))
        self.assertContains(response, 'action="/login/" method="POST"')

    def test_context_given(self):
        response = self.client.get('/login/') 
        # Check if the context contains the expected data
        self.assertTrue(isinstance(response.context['isauth'], bool))
        self.assertTrue(isinstance(response.context['error'], str))

class LoginPOST(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.post("/login/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.post(reverse("Login"))
        self.assertEqual(response.status_code, 200)

    def test_success_login_case(self):
        formdata_example = {
            "username": "LoginTestingSuccess",
            "password": "LoginTestingSuccess",
        }
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

    def test_failure_different_passwords_login_case(self):
        formdata_example = {
            "username": "LoginTestingDifferentPass",
            "password": "LoginTestingDifferentPass",
        }
        self.user = User.objects.create_user(username=formdata_example["username"], password="DIFFERENTPASSWORD")
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

    def test_failure_username_doesnt_exist_login_case(self):
        formdata_example = {
            "username": "LoginUsernameDoesntExist",
            "password": "LoginUsernameDoesntExist",
        }
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

    def test_username_length_login_case(self):
        # username far too short
        formdata_example = {
            "username": "log",
            "password": "TestingUsernameLength_TooShort",
        }
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)

        # username far too long
        formdata_example = {
            "username": ("x" * 120) + "login",
            "password": "TestingUsernameLength",
        }
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)
        
        # username lower boundary -1
        formdata_example["username"] = "logi"
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)

        # username lower boundary
        formdata_example["username"] = "login"
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # username lower boundary +1
        formdata_example["username"] = ("x" * 1) + "login"
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # username upper boundary -1
        formdata_example["username"] = ("x" * 94) + "login"
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # username upper boundary
        formdata_example["username"] = ("x" * 95) + "login"
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # username upper boundary +1
        formdata_example["username"] = ("x" * 96) + "login"
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)

    def test_password_length_login_case(self):
        # password far too short
        formdata_example = {
            "username": "loginTesting",
            "password": "e",
        }
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)

        # password far too long
        formdata_example["username"] = "loginpasswordtoolong"
        formdata_example["password"] = "x" * 502
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)

        # password lower boundary -1
        formdata_example["username"] = "loginpasswordlowerminusone"
        formdata_example["password"] = "x" * 4
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)

        # password lower boundary
        formdata_example["username"] = "loginpasswordlower"
        formdata_example["password"] = "x" * 5
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # password lower boundary +1
        formdata_example["username"] = "loginpasswordlowerplusone"
        formdata_example["password"] = "x" * 6
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # password upper boundary -1
        formdata_example["username"] = "loginpasswordupperminusone"
        formdata_example["password"] = "x" * 99
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # password upper boundary
        formdata_example["username"] = "loginpasswordupper"
        formdata_example["password"] = "x" * 100
        self.user = User.objects.create_user(username=formdata_example["username"], password=formdata_example["password"])
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 302)

        # password upper boundary +1
        formdata_example["username"] = "loginpasswordupperplusone"
        formdata_example["password"] = "x" * 101
        response = self.client.post("/login/", formdata_example)
        self.assertEqual(response.status_code, 200)


