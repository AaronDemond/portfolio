from django.test import TestCase


class IndexViewTests(TestCase):
    def test_index_renders_base_template_with_navigation(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'C. Aaron Demond')
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Privacy')
        self.assertContains(response, 'At a Glance')
        self.assertContains(response, 'View My Work')
        self.assertContains(response, 'Download CV')
        self.assertContains(response, 'Skills')
        self.assertContains(response, 'TypeScript')
        self.assertContains(response, 'CI/CD')
        self.assertNotContains(response, '2025 Alex Morgan')
