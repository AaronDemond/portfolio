from django.shortcuts import render

from .project_data import get_project, get_projects


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
