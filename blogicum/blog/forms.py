from django import forms
from django.contrib.auth import get_user_model

from blog.models import ComentPosts, Post

User = get_user_model()


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M:%S',
                attrs={'type': 'datetime-local'}
            )
        }


class ComentPostsForm(forms.ModelForm):

    class Meta:
        model = ComentPosts
        fields = ('text',)
