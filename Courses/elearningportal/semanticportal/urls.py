from django.urls import path
from semanticportal.views import *

urlpatterns = [
    path('', fetch_branches_semantic, name='semantic-branch'),
    path('submit/', submit_result, name='submit_result'),
    path('write-course', write_course, name='write_course'),
    path('select-branches', select_branches, name='select_branches'),
    path('home', display_data, name='semantic_course'),
    path('home-gpt', display_data_gpt, name='chart_gpt_course'),
]
