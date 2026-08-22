import logging
from smtplib import SMTPException

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect

from .forms import ContactForm
from .project_data import get_project, get_projects

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html', {'projects': get_projects()})


def projects(request):
    return render(
        request,
        'projects.html',
        {
            'page_title': 'Projects',
            'projects': get_projects(),
        },
    )


def project_detail(request, project_id):
    project = get_project(project_id)
    return render(
        request,
        'project_detail.html',
        {
            'page_title': project.name,
            'project': project,
        },
    )


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                EmailMessage(
                    subject=f"Portfolio contact: {form.cleaned_data['subject']}",
                    body=(
                        f"Name: {form.cleaned_data['name']}\n"
                        f"Email: {form.cleaned_data['email']}\n\n"
                        f"{form.cleaned_data['message']}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=settings.CONTACT_RECIPIENTS,
                    reply_to=[form.cleaned_data['email']],
                ).send()
            except (OSError, SMTPException):
                logger.exception('Unable to deliver contact form submission.')
                form.add_error(
                    None,
                    'Your message could not be sent. Please try again later.',
                )
            else:
                messages.success(
                    request,
                    'Thanks for your message. I will respond within 24-48 hours.',
                )
                return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'page_title': 'Contact'})
