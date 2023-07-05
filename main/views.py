import json
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse


# Create your views here.


def task_list(request):
    tasks = Task.objects.all()
    task_list = [{'id': task.id, 'title': task.title, 'description': task.description,
                  'completed': task.completed} for task in tasks]
    return JsonResponse(task_list, safe=False)


def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            completed = data.get('completed', False)
            task = Task.objects.create(
                title=title, description=description, completed=completed)
            task.save()
            return JsonResponse({'message': 'Body received successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def update_task(request, task_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task = Task.objects.get(id=task_id)
            for key, value in data.items():
                setattr(task, key, value)
            task.save()
            return JsonResponse({'message': 'Task updated successfully'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
