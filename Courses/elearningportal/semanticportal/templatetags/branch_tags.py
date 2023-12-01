from django import template
from semanticportal.models import *
from django.db.models import Q


register = template.Library()


@register.simple_tag()
def get_branchList():
    return BranchList.objects.all()


@register.simple_tag()
def get_branchUrl(branch):
    return BranchRequest.objects.filter(course=branch).order_by('id')


@register.simple_tag()
def get_branch_text(branch):
    return BranchRequest.objects.filter(branch=branch)


@register.simple_tag()
def save_branchList(branchSlug, caption):
    if not BranchList.objects.filter(branch_name=branchSlug).exists():
        branch_instance = BranchList(branch_name=branchSlug, branch_caption=caption)
        branch_instance.save()


@register.simple_tag()
def is_branch_exists(branch_name):
    return BranchRequest.objects.filter(branch=branch_name).first()


@register.simple_tag()
def save_requested_branches(branch, branch_name, data):
    # Save the data to the database
    branch_data, created = BranchRequest.objects.get_or_create(course=branch, branch=branch_name,
                                                               defaults={'data': data})
    branch_data.data = data
    branch_data.save()


@register.simple_tag()
def get_requested_branch_text(data_list, view=None):
    branch_names = [branch_obj.branch for branch_obj in data_list]
    if view:
        return BranchRequest.objects.filter(branch__in=branch_names).order_by('id')
    else:
        return BranchRequest.objects.filter(branch__in=branch_names).filter(view__isnull=True).order_by('id')

