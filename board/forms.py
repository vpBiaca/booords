from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Topic, Post


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Topic'))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Post'))
