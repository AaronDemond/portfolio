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
        self.assertContains(response, 'GE Tracker')
        self.assertNotContains(response, '2025 Alex Morgan')

    def test_project_card_technologies_use_available_card_space(self):
        stylesheet = (settings.BASE_DIR / 'static' / 'css' / 'projects.css').read_text()

        self.assertIn(
            '.project-card .project-card__technologies {\n'
            "  /* Pushes the muted technology list to the card's lower content area. */\n"
            '  margin-top: auto;',
            stylesheet,
        )


class ProjectsViewTests(TestCase):
    def test_projects_renders_server_provided_project_listing(self):
        response = self.client.get('/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Projects')
        self.assertContains(response, 'Resilient Telemetry Platform')
        self.assertContains(response, 'TileRacer')
        self.assertContains(response, 'GE Tracker')
        self.assertContains(response, 'C++, Python, TypeScript, HTML, CMake, PowerShell')
        self.assertContains(response, 'View Project &#10230;', count=3)
        self.assertContains(response, 'Complete', count=3)
        self.assertContains(response, 'href="#resilient-telemetry-platform"')
        self.assertContains(response, 'class="projects__divider"')
        self.assertContains(response, 'Upcoming')
        self.assertContains(response, 'Near term')
        self.assertContains(response, 'Short term')
        self.assertContains(response, 'Long term')
        self.assertNotContains(response, 'Polish portfolio project case studies')

    def test_index_projects_navigation_points_to_projects_page(self):
        response = self.client.get('/')

        self.assertContains(response, 'href="/projects/"')
