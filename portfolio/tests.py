from django.conf import settings
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
        self.assertContains(response, 'Java')
        self.assertContains(response, 'Cross Platform Development')
        self.assertContains(response, 'Experience Highlights')
        self.assertContains(response, 'View full experience history')
        self.assertContains(response, 'Featured Projects')
        self.assertContains(response, 'Resilient Telemetry Platform')
        self.assertContains(response, 'TileRacer')
        self.assertContains(response, 'TaskPilot')
        self.assertNotContains(response, '2025 Alex Morgan')

    def test_project_card_technologies_use_available_card_space(self):
        stylesheet = (settings.BASE_DIR / 'static' / 'css' / 'base.css').read_text()

        self.assertIn(
            '.project-card .project-card__technologies {\n'
            "  /* Pushes the muted technology list to the card's lower content area. */\n"
            '  margin-top: auto;',
            stylesheet,
        )
