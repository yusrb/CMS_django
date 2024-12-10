from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from .views import PasswordResetViewCustom, PasswordResetDoneViewCustom, PasswordResetConfirmViewCustom, PasswordResetCompleteViewCustom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', include('admin_argon.urls')),
    path('' , include(('user_cms.urls' , 'user_cms') , namespace="user")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('password_reset/', PasswordResetViewCustom.as_view(template_name="user/password_reset.html"), name="user_password_reset"),
    path('password_reset_done/', PasswordResetDoneViewCustom.as_view(template_name="user/password_reset_done.html"), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', PasswordResetConfirmViewCustom.as_view(template_name="user/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password_reset_complete', PasswordResetCompleteViewCustom.as_view(template_name="user/password_reset_complete.html"), name="password_reset_complete"),
    path('admins/' , include(('admin_cms.urls' , 'admin_cms') , namespace="admins")),
    path("__reload__/", include("django_browser_reload.urls")),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)