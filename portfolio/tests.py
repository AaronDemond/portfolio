from smtplib import SMTPException
from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.test import TestCase

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


class ProjectDataTests(ProjectFixtureMixin, TestCase):
    def test_get_projects_includes_all_project_data(self):
        self.project.architecture = 'project_architectures/architecture.pdf'
        self.project.save()
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
        self.assertEqual(
            project_data.architecture.name,
            'project_architectures/architecture.pdf',
        )
        self.assertEqual(project_data.results, ('Reduced latency.',))
        self.assertEqual(
            project_data.key_architecture_decisions,
            ('Use a fault-tolerant architecture.',),
        )
        self.assertEqual(project_data.git_link, self.project.git_link)


class IndexViewTests(ProjectFixtureMixin, TestCase):
    def test_index_renders_base_template_with_navigation(self):
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
        self.assertContains(response, 'Download CV')
        self.assertContains(response, 'Skills')
        self.assertContains(response, 'Java')
        self.assertContains(response, 'Cross Platform Development')
        self.assertContains(response, 'Experience Highlights')
        self.assertContains(response, 'View full experience history')
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
        self.assertEqual(response.context['project'].id, self.project.id)


class ContactViewTests(TestCase):
    def test_contact_page_renders_active_navigation_and_form(self):
        response = self.client.get('/contact/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Send a Message')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'href="/contact/"')

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
        self.assertEqual(mail.outbox[0].reply_to, ['visitor@example.com'])
        self.assertEqual(mail.outbox[0].subject, 'Portfolio contact: Project inquiry')
        self.assertIn('Test Visitor', mail.outbox[0].body)
        self.assertContains(response, 'Thanks for your message.')

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

    def test_delivery_failure_returns_an_error_without_success_confirmation(self):
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
        self.assertNotContains(response, 'Thanks for your message.')
