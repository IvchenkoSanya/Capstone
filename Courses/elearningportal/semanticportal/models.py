from django.db import models


# Create your models here.
class BranchRequest(models.Model):
    course = models.CharField(max_length=255, null=True)
    branch = models.CharField(max_length=255, unique=True)
    data = models.JSONField()
    view = models.JSONField(null=True)

    def __str__(self):
        return self.branch


class BranchList(models.Model):
    branch_name = models.CharField(max_length=255, unique=True)
    branch_caption = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.branch_name