from django import forms
from home.models import Task

#create a form
class TaskForm(forms.ModelForm):
    #create a meta class
    class Meta:
        #specify model to be used
        model = Task
        #specify fields to be used
        fields = [
            "tasktitle",
            "taskdescription",
        ]