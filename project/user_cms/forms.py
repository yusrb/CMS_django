from django import forms
from django.contrib.auth.forms import UserCreationForm
from admin_cms.models import User, Konfigurasi
from user_cms.models import Komen , Balasan, Pertanyaan, Jawaban
from .models import Saran

class UserRegisterForm(UserCreationForm):
    level_choices = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]
    level = forms.ChoiceField(choices=level_choices, required=True)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nama = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('nama', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nama']
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return password2

class SaranForm(forms.ModelForm):
    class Meta:
        model = Saran
        fields = ['isi_saran', 'nama', 'email']

class LevelChoiceForm(forms.Form):
    LEVEL_CHOICES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]
    level = forms.ChoiceField(choices=LEVEL_CHOICES, required=True)

class KomenForm(forms.ModelForm):
    class Meta:
        model = Komen
        fields = ['nama' , 'email', 'pesan']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Balasan
        fields = ['pesan']

class KonfigurasiForm(forms.ModelForm):
    class Meta:
        model = Konfigurasi
        fields = [
            'instagram',
            'facebook',
            'x',
            'linkedin',
            'tiktok',
            'alamat',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'border border-gray-300 rounded-md p-2 w-full'
            })

    @property
    def navbar_color(self):
        return self.cleaned_data.get('navbar_page_color', '#1F2937')

    @property
    def body_color(self):
        return self.cleaned_data.get('body_page_color', '#FFFFFF')

class PertanyaanForm(forms.ModelForm):
    class Meta:
        model = Pertanyaan
        fields = ['judul', 'isi',]

class JawabanForm(forms.ModelForm):
    class Meta:
        model = Jawaban
        fields = ['isi']