from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    architecture = models.FileField(upload_to='project_architectures/', blank=True)
    git_link = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='screenshots',
    )
    file = models.FileField(upload_to='project_screenshots/')

    def __str__(self):
        return f'{self.project.name} screenshot'


class ProjectTool(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tools',
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class ProjectResult(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='results',
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class ProjectKeyArchitectureDecision(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='key_architecture_decisions',
    )
    text = models.TextField()

    def __str__(self):
        return self.text
