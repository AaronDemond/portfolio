from smtplib import SMTPException
from unittest.mock import patch

from django.conf import settings
from django.conf.urls.static import static
from django.core import mail
from django.test import SimpleTestCase, TestCase, override_settings

from .models import (
    Project,
    ProjectKeyArchitectureDecision,
    ProjectResult,
    ProjectScreenshot,
    ProjectTool,
)
from .project_data import get_projects


class ProjectFixtureMixin:
    def setUp(self):
        self.project = Project.objects.create(
            name='Resilient Telemetry Platform',
            description='A distributed search-and-rescue telemetry simulator.',
            git_link='https://github.com/example/resilient-telemetry-platform',
        )
        ProjectTool.objects.bulk_create(
            [
                ProjectTool(project=self.project, text='C++'),
                ProjectTool(project=self.project, text='Python'),
                ProjectTool(project=self.project, text='TypeScript'),
            ],
        )
        self.additional_projects = [
            Project.objects.create(
                name='TileRacer',
                description='A multiplayer RuneLite minigame plugin.',
            ),
            Project.objects.create(
                name='GE Tracker',
                description='An Old School RuneScape portfolio tracker.',
            ),
        ]


class PrivacyViewTests(SimpleTestCase):
    def test_privacy_page_renders_policy_and_footer_navigation(self):
        response = self.client.get('/privacy/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'privacy.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Last updated: August 22, 2026')
        self.assertContains(response, 'If you choose to use the contact form')
        self.assertContains(response, 'DigitalOcean')
        self.assertContains(response, 'href="/privacy/"')
        self.assertNotContains(response, 'Terms')
        self.assertNotContains(response, 'aria-label="LinkedIn"')


class ProjectDataTests(ProjectFixtureMixin, TestCase):
    def test_get_projects_includes_all_project_data(self):
        ProjectScreenshot.objects.create(
            project=self.project,
            file='project_screenshots/overview.png',
        )
        ProjectResult.objects.create(project=self.project, text='Reduced latency.')
        ProjectKeyArchitectureDecision.objects.create(
            project=self.project,
            text='Use a fault-tolerant architecture.',
        )

        project_data = next(
            project_data
            for project_data in get_projects()
            if project_data.id == self.project.id
        )

        self.assertEqual(project_data.id, self.project.id)
        self.assertEqual(project_data.name, self.project.name)
        self.assertEqual(project_data.description, self.project.description)
        self.assertEqual(project_data.tools, ('C++', 'Python', 'TypeScript'))
        self.assertEqual(
            project_data.screenshots[0].name,
            'project_screenshots/overview.png',
        )
        self.assertEqual(project_data.results, ('Reduced latency.',))
        self.assertEqual(
            project_data.key_architecture_decisions,
            ('Use a fault-tolerant architecture.',),
        )
        self.assertEqual(project_data.git_link, self.project.git_link)


class IndexViewTests(ProjectFixtureMixin, TestCase):
    def test_index_renders_base_template_with_navigation(self):
        fourth_project = Project.objects.create(
            name='Hidden Fourth Project',
            description='This project belongs on the full projects page.',
        )
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'C. Aaron Demond')
        self.assertContains(response, 'Home')
        self.assertContains(response, 'href="/contact/"')
        self.assertContains(response, 'Privacy')
        self.assertContains(response, 'At a Glance')
        self.assertContains(response, 'View My Work')
        self.assertContains(response, 'Download Resume')
        self.assertContains(response, 'View GitHub Profile')
        self.assertContains(response, 'href="https://github.com/AaronDemond"')
        self.assertContains(response, 'Skills')
        self.assertContains(response, 'Java')
        self.assertContains(response, 'Cross Platform Development')
        self.assertContains(response, 'Experience Highlights')
        self.assertContains(response, 'Featured Projects')
        self.assertContains(response, 'Resilient Telemetry Platform')
        self.assertContains(
            response,
            'A distributed search-and-rescue telemetry simulator.',
        )
        self.assertContains(response, 'C++, Python, TypeScript')
        self.assertContains(response, f'href="/projects/{self.project.id}/"')
        for project in self.additional_projects:
            self.assertContains(response, f'href="/projects/{project.id}/"')
        self.assertNotContains(response, f'href="/projects/{fourth_project.id}/"')
        self.assertNotContains(response, fourth_project.name)
        self.assertContains(response, 'View Project &#10230;')
        project_data = next(
            project_data
            for project_data in response.context['projects']
            if project_data.id == self.project.id
        )
        self.assertEqual(project_data.name, self.project.name)
        self.assertEqual(
            project_data.tools,
            ('C++', 'Python', 'TypeScript'),
        )
        self.assertNotContains(response, '2025 Alex Morgan')

    def test_project_card_technologies_use_available_card_space(self):
        stylesheet = (settings.BASE_DIR / 'static' / 'css' / 'projects.css').read_text()

        self.assertIn(
            '.project-card .project-card__technologies {\n'
            "  /* Pushes the muted technology list to the card's lower content area. */\n"
            '  margin-top: auto;',
            stylesheet,
        )


class ProjectsViewTests(ProjectFixtureMixin, TestCase):
    def test_projects_renders_server_provided_project_listing(self):
        response = self.client.get('/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Projects')
        self.assertContains(response, 'Resilient Telemetry Platform')
        self.assertContains(
            response,
            'A distributed search-and-rescue telemetry simulator.',
        )
        self.assertContains(response, 'C++, Python, TypeScript')
        self.assertContains(response, f'href="/projects/{self.project.id}/"')
        for project in self.additional_projects:
            self.assertContains(response, f'href="/projects/{project.id}/"')
        self.assertContains(response, 'View Project &#10230;')
        project_data = next(
            project_data
            for project_data in response.context['projects']
            if project_data.id == self.project.id
        )
        self.assertEqual(project_data.name, self.project.name)
        self.assertEqual(
            project_data.tools,
            ('C++', 'Python', 'TypeScript'),
        )

    def test_index_projects_navigation_points_to_projects_page(self):
        response = self.client.get('/')

        self.assertContains(response, 'href="/projects/"')
        self.assertContains(response, 'href="/contact/"')

    def test_project_detail_renders_for_project_id(self):
        response = self.client.get(f'/projects/{self.project.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project_detail.html')
        self.assertContains(response, self.project.name)
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Projects')
        self.assertContains(response, 'href="/contact/"')
        self.assertContains(response, 'Privacy')
        self.assertNotContains(response, 'project-detail__subtitle')
        self.assertNotContains(response, 'Live Demo')
        self.assertContains(response, 'View Code')
        self.assertContains(response, f'href="{self.project.git_link}"')
        self.assertContains(response, 'target="_blank"')
        self.assertContains(response, 'rel="noopener noreferrer"')
        self.assertContains(response, 'Project Summary')
        self.assertContains(response, 'Tech Stack')
        self.assertContains(response, 'Screenshots')
        self.assertContains(response, 'Architecture Overview')
        self.assertNotContains(response, '<h2>Results</h2>')
        self.assertNotContains(response, 'data-carousel-previous')
        self.assertNotContains(response, 'data-carousel-next')
        self.assertNotContains(response, 'Screenshot placeholder')
        self.assertNotContains(response, 'screenshot--placeholder')
        self.assertContains(response, 'No screenshots have been added.')
        self.assertEqual(response.context['project'].id, self.project.id)
        self.assertEqual(response.context['project'].git_link, self.project.git_link)

    def test_project_detail_renders_screenshot_media_urls_from_context(self):
        screenshot = ProjectScreenshot.objects.create(
            project=self.project,
            file='project_screenshots/overview.png',
        )
        ProjectScreenshot.objects.create(
            project=self.project,
            file='project_screenshots/workflow.png',
        )

        response = self.client.get(f'/projects/{self.project.id}/')

        self.assertEqual(
            response.context['project'].screenshots[0].url,
            '/media/project_screenshots/overview.png',
        )
        self.assertContains(
            response,
            f'src="{screenshot.file.url}"',
        )
        self.assertContains(response, 'data-screenshot-preview-trigger')
        self.assertContains(response, 'data-carousel-card', count=2)
        self.assertNotContains(response, 'Screenshot placeholder')
        self.assertNotContains(response, 'screenshot--placeholder')
        self.assertContains(response, 'data-screenshot-preview')
        self.assertContains(response, 'data-screenshot-preview-close')
        self.assertContains(response, 'aria-label="Close Screenshot"')
        self.assertContains(response, 'Close Screenshot')
        self.assertContains(response, 'js/screenshot-preview.js')

    def test_project_detail_renders_architecture_decisions_above_screenshots(self):
        ProjectKeyArchitectureDecision.objects.bulk_create(
            [
                ProjectKeyArchitectureDecision(
                    project=self.project,
                    text='Separate ingestion from telemetry processing.',
                ),
                ProjectKeyArchitectureDecision(
                    project=self.project,
                    text='Persist events before downstream delivery.',
                ),
            ],
        )
        ProjectResult.objects.create(
            project=self.project,
            text='Reduced telemetry processing latency.',
        )

        response = self.client.get(f'/projects/{self.project.id}/')

        self.assertContains(response, 'Separate ingestion from telemetry processing.')
        self.assertContains(response, 'Persist events before downstream delivery.')
        self.assertNotContains(response, 'Reduced telemetry processing latency.')
        self.assertLess(
            response.content.index(b'Architecture Overview'),
            response.content.index(b'Screenshots'),
        )
        self.assertNotContains(response, '<strong>Client</strong>')
        self.assertNotContains(response, 'Lorem ipsum dolor sit amet.</li>')


class MediaConfigurationTests(SimpleTestCase):
    def test_media_urls_are_served_from_the_media_root(self):
        with override_settings(DEBUG=True):
            media_patterns = static(
                settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT,
            )
        match = media_patterns[0].resolve(
            'media/project_screenshots/overview.png'
        )

        self.assertEqual(settings.MEDIA_URL, '/media/')
        self.assertEqual(settings.MEDIA_ROOT, settings.BASE_DIR / 'media')
        self.assertEqual(match.kwargs['path'], 'project_screenshots/overview.png')
        self.assertEqual(match.kwargs['document_root'], settings.MEDIA_ROOT)


class ContactViewTests(TestCase):
    def test_contact_page_renders_active_navigation_and_form(self):
        response = self.client.get('/contact/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Send a Message')
        self.assertContains(response, 'I reply within 48 hours.')
        self.assertNotContains(response, 'Response Time')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'href="/contact/"')
        self.assertContains(response, 'href="/privacy/"')
        self.assertNotContains(response, 'Terms')
        footer = response.content.decode().split('<footer', 1)[1]
        self.assertNotIn('aria-label="LinkedIn"', footer)
        self.assertNotContains(response, 'tel:')
        self.assertNotContains(response, 'mailto:')
        self.assertContains(response, 'https://www.linkedin.com/in/aarondemond', count=2)
        self.assertContains(response, 'https://github.com/AaronDemond')
        self.assertContains(response, 'https://x.com/AaronDemond', count=2)
        self.assertContains(response, 'Monday-Friday')
        self.assertContains(response, '9:00 AM-6:00 PM Atlantic Time')
        self.assertContains(response, 'aria-label="Social profiles"')
        self.assertNotContains(response, 'Frequently Asked')
        self.assertNotContains(
            response,
            "Have a project in mind or want to say hello? I'd love to hear from you.",
        )

    def test_contact_submission_delivers_to_configured_recipients(self):
        response = self.client.post(
            '/contact/',
            {
                'name': 'Test Visitor',
                'email': 'visitor@example.com',
                'subject': 'Project inquiry',
                'message': 'I would like to discuss a project.',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, list(settings.CONTACT_RECIPIENTS))
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].reply_to, ['visitor@example.com'])
        self.assertEqual(mail.outbox[0].subject, 'Portfolio contact: Project inquiry')
        self.assertIn('Test Visitor', mail.outbox[0].body)
        self.assertContains(
            response,
            'Thank you for reaching out. I will respond within 48 hours.',
        )
        self.assertContains(response, 'data-contact-success-dialog')

    def test_invalid_contact_submission_preserves_errors_without_delivery(self):
        response = self.client.post(
            '/contact/',
            {
                'name': 'Test Visitor',
                'email': 'not-an-email',
                'subject': 'Project inquiry',
                'message': 'I would like to discuss a project.',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, 'Enter a valid email address.')

    @override_settings(DEBUG=True)
    def test_delivery_failure_returns_the_smtp_error_in_debug_mode(self):
        with patch(
            'portfolio.views.EmailMessage.send',
            side_effect=SMTPException('SMTP server unavailable'),
        ):
            response = self.client.post(
                '/contact/',
                {
                    'name': 'Test Visitor',
                    'email': 'visitor@example.com',
                    'subject': 'Project inquiry',
                    'message': 'I would like to discuss a project.',
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your message could not be sent:')
        self.assertContains(response, 'SMTP server unavailable')
        self.assertNotContains(response, 'Thanks for your message.')

    @override_settings(DEBUG=False)
    def test_delivery_failure_hides_the_smtp_error_outside_debug_mode(self):
        with patch(
            'portfolio.views.EmailMessage.send',
            side_effect=SMTPException('SMTP server unavailable'),
        ):
            response = self.client.post(
                '/contact/',
                {
                    'name': 'Test Visitor',
                    'email': 'visitor@example.com',
                    'subject': 'Project inquiry',
                    'message': 'I would like to discuss a project.',
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your message could not be sent.')
        self.assertNotContains(response, 'SMTP server unavailable')
