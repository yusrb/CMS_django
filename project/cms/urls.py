from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', include('admin_argon.urls')),
    path('' , include(('user_cms.urls' , 'user_cms') , namespace="user")),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name="user_password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_done.html"), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>' , auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"), name="password_reset_complete"),
    path('admins/' , include(('admin_cms.urls' , 'admin_cms') , namespace="admins")),
    path("__reload__/", include("django_browser_reload.urls")),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)