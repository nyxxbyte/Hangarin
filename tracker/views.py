from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, SubTask, Note, Goal
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Note, Goal 

def update_note(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id)  
        note.title = request.POST.get('title', note.title)
        note.content = request.POST.get('content', note.content)
        note.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def update_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id) 
        new_progress = request.POST.get('progress')
        if new_progress != "" and new_progress is not None:
            goal.progress = int(new_progress)
            goal.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def dashboard(request):
    # Your existing dashboard logic here
    return render(request, 'tracker/index.html')

DEFAULT_PILLARS = [
    {
        'title': 'Academic Arc',
        'category': 'study',
        'subtasks': ['ComSci Project', 'Review Lecture Notes']
    },
    {
        'title': 'Headspace',
        'category': 'mental',
        'subtasks': ['Take a break from socmed', '10 mins meditation']
    },
    {
        'title': 'Body & Health',
        'category': 'physical',
        'subtasks': ['Take a walk or exercise', '10 mins stretching']
    },
    {
        'title': 'Nourish & Hydrate',
        'category': 'food',
        'subtasks': ['Drink water (8 glasses)', 'Eat a healthy meal']
    }
]

def ensure_default_tasks():
    if not Task.objects.exists():
        for item in DEFAULT_PILLARS:
            task = Task.objects.create(
                title=item['title'],
                category=item['category'],
                is_default=True
            )
            for sub_title in item['subtasks']:
                SubTask.objects.create(task=task, title=sub_title)

# --- Navigation & Pages ---

def dashboard_view(request):
    ensure_default_tasks()
    context = {
        'tasks': Task.objects.all(),
        'active_tab': 'dashboard'
    }
    return render(request, 'dashboard.html', context)

def notes_view(request):
    context = {
        'notes': Note.objects.all().order_by('-created_at'),
        'active_tab': 'notes'
    }
    return render(request, 'dashboard.html', context)

def goals_view(request):
    context = {
        'goals': Goal.objects.all(),
        'active_tab': 'goals'
    }
    return render(request, 'dashboard.html', context)

def settings_view(request):
    return render(request, 'dashboard.html', {'active_tab': 'settings'})

# --- Dashboard Actions ---

def toggle_subtask(request, subtask_id):
    subtask = SubTask.objects.filter(id=subtask_id).first()
    if subtask:
        # Check actual database field names on SubTask
        field_names = [f.name for f in subtask._meta.get_fields()]
        if 'is_completed' in field_names:
            subtask.is_completed = not subtask.is_completed
        elif 'completed' in field_names:
            subtask.completed = not subtask.completed
        subtask.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def delete_subtask(request, subtask_id):
    subtask = SubTask.objects.filter(id=subtask_id).first()
    if subtask:
        subtask.delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def add_subtask(request, task_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        if title:
            task = get_object_or_404(Task, id=task_id)
            SubTask.objects.create(
                task=task,
                title=title.strip(),
                due_date=due_date if due_date else None
            )
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def replace_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('dashboard')

def add_custom_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category', 'custom')
        if title and title.strip():
            Task.objects.create(title=title.strip(), category=category.strip() or 'custom', is_default=False)
    return redirect('dashboard')

def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('dashboard')

# --- Lore Dump Actions ---

def add_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Note.objects.create(title=title.strip(), content=content.strip())
    return redirect('notes')

def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('notes')

# --- The Vision Actions ---

def add_goal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        target_date = request.POST.get('target_date')
        progress = request.POST.get('progress', 0)
        if title:
            Goal.objects.create(
                title=title.strip(),
                target_date=target_date if target_date else None,
                progress=int(progress) if progress else 0
            )
    return redirect('goals')

def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    goal.delete()
    return redirect('goals')

# --- Control Center Actions ---

def clear_completed_tasks(request):
    SubTask.objects.filter(is_completed=True).delete()
    return redirect('dashboard')

def reset_all_data(request):
    Task.objects.all().delete()
    Note.objects.all().delete()
    Goal.objects.all().delete()
    ensure_default_tasks()
    return redirect('dashboard')