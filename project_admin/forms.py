from django import forms
from .models import Project, Work


class ProjectForm ( forms . ModelForm):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'objective']
        widgets = {
            'project_id': forms.TextInput(attrs={'placeholder': 'Project ID'}),
            'project_name': forms.TextInput(attrs={'placeholder': 'Project Name'}),
            'objective': forms.Textarea(attrs={'placeholder': 'Project Objective'})
        }

    # def clean_project_id(self, *args, **kwargs):
    #     try:
    #         Project.objects.get(project_id=self.cleaned_data['project_id'])
    #     except Project.DoesNotExist:
    #         return self.cleaned_data['project_id']
    #     raise forms.ValidationError("Project Id already exist..")


class ProgramerForm ( forms . ModelForm):
    class Meta:
        model = Work
        fields = ['project_id', 'programmer_id', 'task', 'file']
        widgets = {
            'project_id': forms.HiddenInput(),
            'programmer_id': forms.Select(attrs={'class': 'form-control input-block', 'placeholder': 'Programmer Name'}),
            'task': forms.Textarea(attrs={'class': 'form-control input-block', 'placeholder': 'Objective of Programmer'}),
            'file': forms.FileInput(attrs={'class': 'form-control input-block', 'placeholder': 'Choose file'})
        }