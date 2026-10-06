from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import STATUS_CHOICES, Category, Priority, Task


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "registration/../templates/account/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")


@login_required
def home(request):
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    category = request.GET.get("category", "")

    tasks = (
        Task.objects.select_related("category", "priority")
        .prefetch_related("subtasks", "notes")
        .order_by("deadline")
    )
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status:
        tasks = tasks.filter(status=status)
    if priority.isdigit():
        tasks = tasks.filter(priority_id=priority)
    if category.isdigit():
        tasks = tasks.filter(category_id=category)

    context = {
        "tasks": tasks,
        "q": q,
        "status": status,
        "priority": priority,
        "category": category,
        "status_choices": STATUS_CHOICES,
        "priorities": Priority.objects.all(),
        "categories": Category.objects.all(),
        "filtered": any([q, status, priority, category]),
    }
    return render(request, "tasks/home.html", context)


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Task added.")
        return redirect("home")
    return render(request, "tasks/task_form.html", {"form": form})


@login_required
@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect("home")