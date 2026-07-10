from typing import Self
from django import forms

from posts.models import Post

#
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ["title", "content", "rate", "image"]


class PostForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(min_length=30)
    rate = forms.IntegerField(min_value=1, max_value=10)
    image = forms.ImageField(required=False)

    def clean_title(self):
        data = self.cleaned_data["title"]

        # 2. Делаем
        if "war" in data:
            raise forms.ValidationError("this is banned word!")

        return data
