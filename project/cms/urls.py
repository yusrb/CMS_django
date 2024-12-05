from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', include('admin_argon.urls')),
    path('' , include(('user_cms.urls' , 'user_cms') , namespace="user")),
    path('admins/' , include(('admin_cms.urls' , 'admin_cms') , namespace="admins")),
    path("__reload__/", include("django_browser_reload.urls")),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)