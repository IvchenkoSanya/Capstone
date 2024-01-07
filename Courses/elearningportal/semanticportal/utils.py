import json

import requests
from bs4 import BeautifulSoup
from django.core.serializers import serialize

from semanticportal.models import *
from semanticportal.templatetags.branch_tags import *

resultJSON = []
branch = ''


def fetch_branch_global(branch_name):
    global branch
    branch = branch_name


def return_branch_global():
    return branch


def get_data_from_server_and_save():
    url = 'http://semantic-portal.net/branches'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    global branch
    branch = ''

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', class_='caption')
        for link in links:
            href = link.get('href')
            branch = href.split('/')[-1]
            caption = link.find('h3').text.strip()
            save_branchList(branch, caption)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


def fetch_branch(branch_name):
    global branch
    branch = branch_name
    branch_obj = is_branch_exists(branch_name)
    if not branch_obj:
        # Data doesn't exist in the database, fetch it from the server
        fetch_children_recursive_and_save(branch_name)


def fetch_children_recursive_and_save(branch_name):
    api_url = f'http://semantic-portal.net/api/branch/{branch_name}/children'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        timeout_seconds = 10
        response = requests.get(api_url, headers=headers, timeout=timeout_seconds)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        global branch
        save_requested_branches(branch, branch_name, data)

        # Fetch children recursively
        for child in data:
            fetch_children_recursive_and_save(child['view'])
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")


def fetch_empty_views_and_save(items):
    data_list = []
    for key, value in items.items():
        for branch_obj in value:
            data_list.append(branch_obj)

    branches_without_view = get_requested_branch_text(data_list, view=False)

    for item in branches_without_view:
        item.view = fetch_branch_view(item.branch)
        item.save()

    return generate_json_file(data_list)


def fetch_branch_view(branch_name):

    api_url = f'http://semantic-portal.net/api/branch/{branch_name}/view'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    print(api_url)
    try:
        timeout_seconds = 10
        response = requests.get(api_url, headers=headers, timeout=timeout_seconds)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data

    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")


def generate_course_json_manually(items):
    global resultJSON
    resultJSON = []
    course = items['course']
    resultJSON.append({
        "query": course,
        "llm_version": "gpt_4",
        "language": "English",
        "course_content": {
            "course_name": f'A tour of the {course} language',
            "lessons": [],
            "content": {}
        }
    })

    title_list = items['topic'].split('\r\n')

    for title in title_list:
        resultJSON[0]['course_content']['lessons'].append({'title': title, 'topics': []})
    save_json(course)
    return resultJSON


def generate_json_file(data_list):

    global resultJSON
    resultJSON = []
    init_json()

    branch_requests = get_requested_branch_text(data_list, view=True)

    result_json = serialize('json', branch_requests)
    result_data = json.loads(result_json)

    for item in result_data:
        if item['fields']['view'] is not None:
            caption = item['fields']['view']['caption']
            text = item['fields']['view']['text']
            if text:
                resultJSON[0]['course_content']['lessons'].append({'title': caption, 'topics': []})
                resultJSON[0]['course_content']['content'].append({caption: {'content': text}})

    save_json()
    return resultJSON


def init_json():
    global branch
    initBranch = get_branch_text(branch)
    result_json = serialize('json', initBranch)
    result_data = json.loads(result_json)

    if result_data[0]['fields']['view'] is None:
        view = result_data[0]['fields']['data'][0]['view']
    else:
        view = result_data[0]['fields']['view']['caption']
    contex = result_data[0]['fields']['data'][0]['caption']

    resultJSON.append({
        "query": view,
        "llm_version": "gpt_4",
        "language": "English",
        "course_content": {
        "course_name": contex,
        "lessons": [],
        "content": []
        }
    })

def save_json(course=None):
    global branch
    global resultJSON
    if course:
        filename = f'{course}.json'
    else:
        filename = f'{branch}.json'

    save_json_data_to_course(resultJSON, branch)

    with open(filename, 'w') as f:
        json.dump(resultJSON, f, indent=2)



def save_json_data_to_course(JSON, branch_id):
    try:
        branch, created = BranchList.objects.get_or_create(branch_name=branch_id)
        course, created = Course.objects.get_or_create(course=branch)
        course.semantic_data = JSON
        course.save()

    except Exception as e:
        print(f"Error saving JSON data: {e}")
        return None
