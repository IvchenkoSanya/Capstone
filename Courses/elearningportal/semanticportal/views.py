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
            generate_course_json_manually(form.cleaned_data)
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
            fetch_empty_views_and_save(form.cleaned_data)
    else:
        form = SelectBranches()
    return render(request, 'semanticportal/select_branches.html', {'form': form})
