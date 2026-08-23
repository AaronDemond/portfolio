from dataclasses import dataclass

from django.db.models.fields.files import FieldFile
from django.http import Http404

from .models import Project


@dataclass(frozen=True)
class ProjectData:
    id: int
    name: str
    description: str
    status: str
    status_label: str
    tools: tuple[str, ...]
    screenshots: tuple[FieldFile, ...]
    results: tuple[str, ...]
    key_architecture_decisions: tuple[str, ...]
    git_link: str


def get_projects() -> list[ProjectData]:
    return [_build_project_data(project) for project in _project_queryset()]


def get_project(project_id: int) -> ProjectData:
    try:
        project = _project_queryset().get(pk=project_id)
    except Project.DoesNotExist as error:
        raise Http404('Project not found.') from error

    return _build_project_data(project)


def _project_queryset():
    return Project.objects.prefetch_related(
        'tools',
        'screenshots',
        'results',
        'key_architecture_decisions',
    )


def _build_project_data(project: Project) -> ProjectData:
    return ProjectData(
        id=project.pk,
        name=project.name,
        description=project.description,
        status=project.status,
        status_label=project.get_status_display(),
        tools=tuple(tool.text for tool in project.tools.all()),
        screenshots=tuple(screenshot.file for screenshot in project.screenshots.all()),
        results=tuple(result.text for result in project.results.all()),
        key_architecture_decisions=tuple(
            decision.text for decision in project.key_architecture_decisions.all()
        ),
        git_link=project.git_link,
    )
