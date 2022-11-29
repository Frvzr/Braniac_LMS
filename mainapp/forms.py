from django import forms
from mainapp.models import CourseFeedback


class CourseFeedbackForm(forms.ModelForm):

    class Meta:
        model = CourseFeedback
        fields = ('course', 'user', 'rating', 'feedback',)
        widgets = {
            'course': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'rating': forms.RadioSelect()
        }

    def __init__(self, *args, course=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if course and user:
            self.fields['course'].initial = course.pk
            self.fields['user'].initial = user.pk


class MailFeedbackForm(forms.Form):

    user_id = forms.IntegerField(widget=forms.HiddenInput)
    message = forms.CharField(
        widget=forms.Textarea,
        help_text=("Enter your message"),
        label=("Message"),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["user_id"].initial = user.pk
