from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import *
from .utils import *


@login_required
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

@login_required
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
    print(request.method)
    if request.method == 'POST':
        form = SelectBranches(request.POST)
        if form.is_valid():
            course = fetch_empty_views_and_save(form.cleaned_data)
            return render(request, 'semanticportal/home.html',
                          {'course': course})
    else:
        form = SelectBranches()
    return render(request, 'semanticportal/select_branches.html', {'form': form})


def display_list_courses(requst):
    courses = Course.objects.all()
    print(courses)
    return render(requst, 'semanticportal/course_list.html', {'courses': courses})


def course_detail(request, course_id):

    course = Course.objects.get(id=course_id)

    options_available = [
        'semantic_data' if course.semantic_data is not None else None,
        'chat_gpt_basic' if course.chat_gpt_basic is not None else None,
        'chat_gpt_advance' if course.chat_gpt_advance is not None else None,
    ]

    options_available = list(filter(None, options_available))
    return render(request, 'semanticportal/course_detail.html',
                  {'options_available': options_available, 'id': course_id})


def option_detail(request, course_id, option):
    course = Course.objects.get(id=course_id)

    if (option == 'semantic_data'):
        return render(request, 'semanticportal/home.html', {'course': course.semantic_data})
    elif (option == 'chat_gpt_basic'):
        return render(request, 'semanticportal/home_gpt.html',
                      {'course_content': course.chat_gpt_basic['course_content']})
    else:
        return render(request, 'semanticportal/home_gpt.html',
                      {'course_content': course.chat_gpt_advance['course_content']})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'semanticportal/login.html'

    def get_success_url(self):
        return reverse_lazy('courses_list')


def logout_user(request):
    logout(request)
    return redirect('courses_list')

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

