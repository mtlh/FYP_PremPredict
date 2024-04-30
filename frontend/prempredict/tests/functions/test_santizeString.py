from django.test import TestCase
from prempredict.views.functions.sanitzeString import cleanString

class TestCleanString(TestCase):

    def test_clean_string_basic(self):
        # Test basic functionality of cleanString function.
        input_string = "<script>alert('Hello, world!');</script>"
        expected_output = ""
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_no_script_tags(self):
        # Test when input has no <script> tags.
        input_string = "This is a test string."
        expected_output = "This is a test string."
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_empty_input(self):
        # Test when input is an empty string.
        input_string = ""
        expected_output = ""
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_multiple_script_tags(self):
        # Test when input has multiple <script> tags.
        input_string = "<script>alert('Hello');</script><script>alert('World');</script>"
        expected_output = ""
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_html_entities(self):
        # Test when input contains HTML entities.
        input_string = "&lt;script&gt;alert(&#x27;Hello&#x27;);&lt;/script&gt;"
        expected_output = "&amp;lt;script&amp;gt;alert(&amp;#x27;Hello&amp;#x27;);&amp;lt;/script&amp;gt;"
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_spaces(self):
        # Test when input contains leading/trailing spaces.
        input_string = "   <script>alert('Hello');</script>   "
        expected_output = ""
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_nested_tags(self):
        # Test when input contains nested HTML tags.
        input_string = "<div><script>alert('Hello');</script></div>"
        expected_output = "&lt;div&gt;&lt;/div&gt;"
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_case_insensitive(self):
        # Test when input contains script tags with different cases.
        input_string = "<Script>alert('Hello');</script>"
        expected_output = ""
        self.assertEqual(cleanString(input_string), expected_output)

    def test_clean_string_with_special_chars(self):
        # Test when input contains special characters.
        input_string = "<script>alert('&amp;');</script>"
        expected_output = ""
        self.assertEqual(cleanString(input_string), expected_output)

