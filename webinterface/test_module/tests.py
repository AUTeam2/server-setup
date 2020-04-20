from django.test import TestCase

# Create your tests here.

class TestHome(TestCase):
    """
    Test cases for the test module
    """
    def test_test_homepage_works(self):
        """
        Test that the landing page for the module exists and renders
        """
        response = self.client.get("/test_module/")  #because APPEND_SLASH = True
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_module/home.html')
        self.assertContains(response, 'test-modul')

    def test_info_page(self):
        """
        Test that the info page for the module exists and renders
        """
        response = self.client.get("/test_module/show_info")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_module/status_list.html')

    def test_result_page(self):
        """
        Test that the results page for the module exists and renders
        """
        response = self.client.get("/test_module/show_result")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_module/result_list.html')

