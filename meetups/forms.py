from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import News


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment


# class NewsForm(forms.ModelForm):
#     body = forms.CharField(widget=CKEditorUploadingWidget(), label='Content')
#     class Meta:
#         model = News
#         fields = ('title', 'author', 'image', 'description', 'is_published')
    
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.content = self.cleaned_data['body']  # map body to content
#         if commit:
#             instance.save()
#         return instance

