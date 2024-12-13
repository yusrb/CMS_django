from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from admin_cms.models import Konfigurasi

def admin_redirect(request):
    return redirect('konten/user_cms/')

class PasswordResetViewCustom(auth_views.PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judul'] = 'Reset Kata Sandi'
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context

class PasswordResetDoneViewCustom(auth_views.PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judul'] = 'Pemberitahuan Reset Kata Sandi'
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context

class PasswordResetConfirmViewCustom(auth_views.PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judul'] = 'Konfirmasi Reset Kata Sandi'
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context

class PasswordResetCompleteViewCustom(auth_views.PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judul'] = 'Reset Kata Sandi Selesai'
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context
