from django.db import models
from markdown import markdown


# Create your models here.
class BranchRequest(models.Model):
    course = models.ForeignKey('BranchList', on_delete=models.SET_NULL, null=True)
    branch = models.CharField(max_length=255, unique=True)
    data = models.JSONField()
    view = models.JSONField(null=True)

    def __str__(self):
        return self.branch


class BranchList(models.Model):
    branch_name = models.CharField(max_length=255, unique=True)
    branch_caption = models.CharField(max_length=255)

    def __str__(self):
        return self.branch_name


class Course(models.Model):
    course = models.ForeignKey('BranchList', on_delete=models.SET_NULL, null=True)
    semantic_data = models.JSONField(null=True)
    chat_gpt_basic = models.JSONField(null=True)
    chat_gpt_advance = models.JSONField(null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.course.branch_caption