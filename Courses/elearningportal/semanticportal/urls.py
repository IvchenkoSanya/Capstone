from django.urls import path
from semanticportal.views import *

urlpatterns = [
    path('semantic-branches', fetch_branches_semantic, name='semantic-branch'),
    path('submit/', submit_result, name='submit_result'),
    path('write-course', write_course, name='write_course'),
    path('select-branches', select_branches, name='select_branches'),
    path('home', display_data, name='semantic_course'),
    path('home-gpt', display_data_gpt, name='chart_gpt_course'),
    path('', display_list_courses, name='courses_list'),
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('courses/<int:course_id>/<str:option>/', option_detail, name='option_detail'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
]
