from django import forms
from .models import Category, Comment
from django.forms.models import ModelMultipleChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


    
class MyMultipleModelChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return "%s" % (obj.name)



class BlogForm(forms.Form):
    category_names = []
    
    title = forms.CharField(label='Blog Title', max_length=30)
    description = forms.CharField(label='Blog Description', max_length=200)
    img = forms.ImageField(label='Image thumbnail')
    category = MyMultipleModelChoiceField(
        label='Tags', 
        widget=forms.CheckboxSelectMultiple, 
        queryset=Category.objects.all(), 
        help_text="If your desired tag is not defined then create tag first")
    content = forms.CharField(label='Blog Content', max_length=5000, widget=forms.Textarea())        


class CreateUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class TagForm(forms.Form):
    name = forms.CharField(label='Tag Name', max_length=30)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class SearchForm(forms.Form):
    search = forms.CharField(label='search', max_length='500', required=False)