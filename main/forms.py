from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]

        widgets = {
            "first_name": forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            "last_name": forms.TextInput(attrs={ 'placeholder': 'Enter your last name'}),
            "email": forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            "gender": forms.NumberInput(attrs={ 'placeholder': 'Enter your phone number'}),
            "address": forms.TextInput(attrs={'placeholder': 'Enter your message'})
        }



class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields




class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'dateend', 'message', 'title', 'address', 'type', 'conducted', 'level' ]
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
        widgets = {
            'dateend': DateInput(attrs={'type': 'date'}),
        }


class CompetencyJournalStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CompetencyJournalStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CompetencyJournal
        fields = ['date',  'title','conducted', 'address', 'learnings',   'type',  'level' ]
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields



class StaffAddFormalForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(StaffAddFormalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Formal
        fields = ['title', 'address', 'conducted', 'date_ended', 'time_duration', 'date_started']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
        widgets = {
            'date_end': DateInput(attrs={'type': 'date'}),
        }
