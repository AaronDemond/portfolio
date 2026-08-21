from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def projects(request):
    project_list = [
        {
            'slug': 'resilient-telemetry-platform',
            'title': 'Resilient Telemetry Platform',
            'description': (
                'A distributed search-and-rescue telemetry simulator designed '
                'for fault tolerance, deterministic scenario replay, and '
                'cross-platform operation.'
            ),
            'technologies': 'C++, Python, TypeScript, HTML, CMake, PowerShell',
        },
        {
            'slug': 'tileracer',
            'title': 'TileRacer',
            'description': (
                'A single- and multiplayer RuneLite minigame plugin with '
                'real-time circuit competition and server-coordinated players.'
            ),
            'technologies': 'Java, Python, WebSockets, PowerShell',
        },
        {
            'slug': 'ge-tracker',
            'title': 'GE Tracker',
            'description': (
                'A Django application for Old School RuneScape portfolio '
                'management, market analysis, alerts, and research tools.'
            ),
            'technologies': 'Django, Python, JavaScript, Cron',
        },
    ]

    return render(
        request,
        'projects.html',
        {
            'page_title': 'Projects',
            'projects': project_list,
        },
    )
