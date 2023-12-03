from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from .utils import *


def fetch_branches_semantic(request):
    # Take all data from semantic portal and save to DB - BranchList
    get_data_from_server_and_save()

    return render(request, 'semanticportal/display_branches_semantic.html')


def submit_result(request):
    print(request)
    if request.method == 'POST':
        selected_branch = request.POST.get('branches')
        fetch_branch(selected_branch)
        return render(request, 'semanticportal/submit_result.html', {'selected_branch': selected_branch})


def write_course(request):
    print(request.method)
    if request.method == 'POST':
        form = WriteCourseTopic(request.POST)
        if form.is_valid():
            course = generate_course_json_manually(form.cleaned_data)
            return render(request, 'semanticportal/home.html',
                          {'course': course})
        else:
            form = WriteCourseTopic()
    else:
        form = WriteCourseTopic()
    return render(request, 'semanticportal/write_course.html', {'form': form})


def select_branches(request):
    print('--------------')
    print(request.method)
    print('--------------')
    if request.method == 'POST':
        form = SelectBranches(request.POST)
        if form.is_valid():
            course = fetch_empty_views_and_save(form.cleaned_data)
            print(course)
            return render(request, 'semanticportal/home.html',
                          {'course': course})
    else:
        form = SelectBranches()
    return render(request, 'semanticportal/select_branches.html', {'form': form})


def display_json(request, course_instance):
    context = {'semantic_data': course_instance.semantic_data}
    return render(request, 'semanticportal/display_json_result.html', context)


def display_data(request):
    # Fetch all courses from the database
    print(return_branch_global())
    course = Course.objects.get(id=1)

    options_available = [
        'semantic_data' if course.semantic_data is not None else None,
        'chat_gpt_basic' if course.chat_gpt_basic is not None else None,
        'chat_gpt_advance' if course.chat_gpt_advance is not None else None,
    ]

    # Remove None values from the list
    options_available = list(filter(None, options_available))

    return render(request, 'semanticportal/home.html', {'options_available': options_available,
                                                        'course': course.semantic_data})


def display_data_gpt(request):
    # Fetch all courses from the database
    print(return_branch_global())
    course = Course.objects.get(id=1)

    options_available = [
        'semantic_data' if course.semantic_data is not None else None,
        'chat_gpt_basic' if course.chat_gpt_basic is not None else None,
        'chat_gpt_advance' if course.chat_gpt_advance is not None else None,
    ]

    # Remove None values from the list
    options_available = list(filter(None, options_available))

    return render(request, 'semanticportal/home_gpt.html',
                  {'course_content': course.chat_gpt_basic['course_content']})

