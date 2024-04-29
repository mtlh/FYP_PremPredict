from django.urls import reverse
from django.test import TestCase

class SignUpGET(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Signup"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("Signup"))
        self.assertTemplateUsed(response, "signup.html")

    def test_template_content(self):
        response = self.client.get(reverse("Signup"))
        self.assertContains(response, 'action="/signup/" method="POST"')

    def test_context_given(self):
        response = self.client.get('/signup/') 
        # Check if the context contains the expected data
        self.assertTrue(isinstance(response.context['isauth'], bool))
        self.assertTrue(isinstance(response.context['error'], str))

class SignUpPOST(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.post("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.post(reverse("Signup"))
        self.assertEqual(response.status_code, 200)

    def test_success_signup_case(self):
        formdata_example = {
            "username": "Testing",
            "email": "Testing@gmail.com",
            "password": "Testing",
            "confpassword": "Testing"
        }
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

    def test_failure_different_passwords_signup_case(self):
        formdata_example = {
            "username": "TestingDifferentPasswords",
            "email": "Testing@gmail.com",
            "password": "Testing1",
            "confpassword": "Testing2"
        }
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

    def test_failure_existing_username_signup_case(self):
        formdata_example = {
            "username": "Testing",
            "email": "Testing@gmail.com",
            "password": "Testing",
            "confpassword": "Testing"
        }
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

    def test_failure_username_length_signup_case(self):
        # username far too short
        formdata_example = {
            "username": "Te",
            "email": "Testing@gmail.com",
            "password": "Testing",
            "confpassword": "Testing"
        }
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

        # username far too long
        formdata_example["username"] = "EXAMPLE" * 100
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)
        
        # username lower boundary -1
        formdata_example["username"] = "x" * 4
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

        # username lower boundary
        formdata_example["username"] = "x" * 5
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # username lower boundary +1
        formdata_example["username"] = "x" * 6
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # username upper boundary -1
        formdata_example["username"] = "x" * 99
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # username upper boundary
        formdata_example["username"] = "x" * 100
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # username upper boundary +1
        formdata_example["username"] = "x" * 101
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

    def test_failure_password_length_signup_case(self):
        # password far too short
        formdata_example = {
            "username": "Testing",
            "email": "Testing@gmail.com",
            "password": "e",
            "confpassword": "e"
        }
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

        # password far too long
        formdata_example["username"] = "passwordtoolong"
        formdata_example["password"] = "x" * 502
        formdata_example["confpassword"] = "x" * 502
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

        # password lower boundary -1
        formdata_example["username"] = "passwordlowerminusone"
        formdata_example["password"] = "x" * 4
        formdata_example["confpassword"] = "x" * 4
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

        # password lower boundary
        formdata_example["username"] = "passwordlower"
        formdata_example["password"] = "x" * 5
        formdata_example["confpassword"] = "x" * 5
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # password lower boundary +1
        formdata_example["username"] = "passwordlowerplusone"
        formdata_example["password"] = "x" * 6
        formdata_example["confpassword"] = "x" * 6
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # password upper boundary -1
        formdata_example["username"] = "passwordupperminusone"
        formdata_example["password"] = "x" * 99
        formdata_example["confpassword"] = "x" * 99
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # password upper boundary
        formdata_example["username"] = "passwordupper"
        formdata_example["password"] = "x" * 100
        formdata_example["confpassword"] = "x" * 100
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 302)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertTrue(response)

        # password upper boundary +1
        formdata_example["username"] = "passwordupperplusone"
        formdata_example["password"] = "x" * 101
        formdata_example["confpassword"] = "x" * 101
        response = self.client.post("/signup/", formdata_example)
        self.assertEqual(response.status_code, 200)
        response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
        self.assertFalse(response)

    def test_failure_email_valid_signup_case(self):
        # Valid email addresses
        valid_emails = [
            "testing@example.com",
            "abc@abc.com",
            "user123@gmail.com",
            "john.doe@company.com",
        ]
        # Invalid email addresses
        invalid_emails = [
            "invalid-email",  # Missing domain
            "user@.com",       # Missing domain name
            "user@domain",     # Missing top-level domain
            "user@dom@ain.com", # Multiple @ symbols
        ]
        for email in valid_emails:
            formdata_example = {
                "username": email,
                "email": email,
                "password": "Testing",
                "confpassword": "Testing"
            }
            response = self.client.post("/signup/", formdata_example)
            self.assertEqual(response.status_code, 302)
            response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
            self.assertTrue(response)

        for email in invalid_emails:
            formdata_example = {
                "username": email,
                "email": email,
                "password": "Testing",
                "confpassword": "Testing"
            }
            response = self.client.post("/signup/", formdata_example)
            self.assertEqual(response.status_code, 200)
            response = self.client.login(username=formdata_example["username"], password=formdata_example["password"])
            self.assertFalse(response)


