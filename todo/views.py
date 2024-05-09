from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.urls import reverse


# Create your views here.


def dashboard(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(owner=request.user).order_by('-created_at')
        p = Paginator(tasks, 5)
        page = request.GET.get('page')
        page_tasks = p.get_page(page)
        context = {
            'tasks': tasks,
            'page_tasks': page_tasks
        }
        return render(request, 'todo/dashboard.html', context)
    else:
        return redirect('todo:login')


def add_task(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')

        if name:
            Task.objects.create(name=name, owner=request.user)
            return redirect('todo:dashboard')

    return redirect('todo:dashboard')


@login_required
def details(request, pk):
    task = Task.objects.get(owner=request.user, pk=pk)

    return render(request, 'todo/details.html', {'task': task})


@login_required
def edit_task(request, pk):
    task = Task.objects.get(owner=request.user, pk=pk)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        go_to_page = previous_page
    else:
        go_to_page = reverse('todo:details', args=[pk])
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        status = request.POST.get('status', '')
        if status == 'Todo':
            is_done = False
        else:
            is_done = True

        if name:
            task.name = name
            task.description = description
            task.is_done = is_done
            task.save()

            return redirect(reverse('todo:details', args=[pk]))

    context = {'task': task, 'go_to_page': go_to_page}
    return render(request, 'todo/edit.html', context)


def delete_task(request, pk):
    task = Task.objects.get(owner=request.user, pk=pk)
    task.delete()

    return redirect('todo:dashboard')


def mark_done(request, pk):
    task = Task.objects.get(owner=request.user, pk=pk)
    task.is_done = True

    task.save()

    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect('todo:dashboard')


def mark_todo(request, pk):
    task = Task.objects.get(owner=request.user, pk=pk)
    task.is_done = False

    task.save()

    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect('todo:dashboard')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('todo:dashboard')
            else:
                return render(request, 'todo/login.html', {'form': form, 'error': 'Invalid username or password chuchu.'})

        else:
            return render(request, 'todo/login.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'todo/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('todo:dashboard')

    else:
        form = SignUpForm()

    return render(request, 'todo/register.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('todo:login')


def paginator_views(request):
    tasks = Task.objects.get(owner=request.user)
    paginator = Paginator(tasks, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'todo/dashboard2.html', {'page_obj': page_obj, 'tasks': tasks})
