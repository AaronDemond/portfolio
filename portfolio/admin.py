from django.contrib import admin

from .models import (
    Project,
    ProjectKeyArchitectureDecision,
    ProjectResult,
    ProjectScreenshot,
    ProjectTool,
)


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1


class ProjectToolInline(admin.TabularInline):
    model = ProjectTool
    extra = 1


class ProjectResultInline(admin.TabularInline):
    model = ProjectResult
    extra = 1


class ProjectKeyArchitectureDecisionInline(admin.TabularInline):
    model = ProjectKeyArchitectureDecision
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'git_link')
    search_fields = ('name', 'description', 'git_link')
    inlines = (
        ProjectScreenshotInline,
        ProjectToolInline,
        ProjectResultInline,
        ProjectKeyArchitectureDecisionInline,
    )
