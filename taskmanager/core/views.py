from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task, ActivityLog
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'core/dashboard.html', {'projects': projects})


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'core/project_list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    tasks = project.tasks.all()
    return render(request, 'core/project_detail.html', {'project': project, 'tasks': tasks})


@login_required
def add_task(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        assigned_to_id = request.POST.get('assigned_to')
        assigned_to = User.objects.get(pk=assigned_to_id) if assigned_to_id else None
        Task.objects.create(project=project, title=title, description=description, assigned_to=assigned_to)
        ActivityLog.objects.create(user=request.user, project=project, action=f"Added task: {title}")
        return redirect('project_detail', pk=pk)
    users = User.objects.all()
    return render(request, 'core/add_task.html', {'project': project, 'users': users})
