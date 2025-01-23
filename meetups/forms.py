from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Meetups, News, Comment
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.core.exceptions import ValidationError
# from django.forms.widgets import SplitDateTimeWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            "content": "Your comment"
        }

class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetups
        fields = (
            'title',
            'organizer',
            'tags',
            'description',
            # 'image',
            'event_date',
            'is_online',
            'link',
            'country',
            'city',
            'location',
        )
        widgets = {
            'event_date': DateTimePickerInput(
                format='%Y-%m-%d %H:%M:%S',
                options={
                    'sideBySide': True,
                    'showClose': True,
                    'showClear': True,
                    'showTodayButton': True,
                },
                attrs={
                    'data-date-format': 'YYYY-MM-DD HH:mm:ss',
                    'data-date-autoclose': 'true',
                }
            ),
        }
    
    def save(self, commit=True):
        meetup = super().save(commit=False)
        meetup.is_published = True
        if commit:
            meetup.save()
        return meetup

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_published'):
            if not cleaned_data.get('title') or not cleaned_data.get('organizer') or not cleaned_data.get('event_date'):
                raise ValidationError("Please fill in all required fields before publishing.")
        return cleaned_data

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

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