from django import forms

from semanticportal.templatetags.branch_tags import get_branchUrl
from semanticportal.utils import return_branch_global


class WriteCourseTopic(forms.Form):
    course = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'input-form', 'placeholder': 'Java'}))
    topic = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'row': 10,
                                                         'placeholder': 'Input\nOutput\nArrays\nInheritance\nObject as a Superclass\nInterface\nCollections'}))


class SelectBranches(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelectBranches, self).__init__(*args, **kwargs)
        self.fields['branch'].queryset = get_branchUrl(return_branch_global())

    branch = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select','style': 'height: 15px; width: 15px;'}))

        
        
