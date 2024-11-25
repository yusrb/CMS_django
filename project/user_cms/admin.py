from django.contrib import admin
from django.utils.timezone import localtime
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from admin_cms.models import User, Aktivitas, Kategori, Carousel, Konfigurasi, Galeri
from user_cms.models import Konten
from user_cms.models import Saran , Komen , Reply
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'nama', 'email', 'level', 'theme')
    list_filter = ('is_active', 'is_staff', 'level', 'telepon')
    search_fields = ('username', 'email', 'nama')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('nama', 'email', 'telepon', 'level')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(id=request.user.id)

class AktivitasAdmin(admin.ModelAdmin):
    list_display = ('user', 'aksi', 'tanggal')
    list_filter = ('user',)
    search_fields = ('user__username', 'aksi')
    ordering = ('-tanggal',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(user__is_superuser=True)

class KontenAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'formatted_tanggal', 'dilihat', 'username')
    search_fields = ('judul',)
    readonly_fields = ['dilihat', 'user', 'username', 'slug']

    def formatted_tanggal(self, obj):
        return localtime(obj.tanggal).strftime('%d %b %Y, %H:%M WIB')
    formatted_tanggal.short_description = 'Tanggal'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user 
            obj.username = request.user.username
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return obj.user == request.user or request.user.is_superuser
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return obj.user == request.user or request.user.is_superuser
        return True

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return obj.user == request.user or request.user.is_superuser
        return True

class KonfigurasiAdmin(admin.ModelAdmin):
    readonly_fields = ['tampil_user']

    fieldsets = (
        (None, {
            'fields': ('tampil_user',),
        }),
        ('Informasi Website', {
            'fields': ('judul_website', 'x' ,'instagram', 'linkedin' ,'facebook', 'tiktok', 'alamat', 'email' , 'iklan' , 'url_iklan')
        }),
    )

    def tampil_user(self, obj):
        return format_html(f'{obj.user} <span style="color: gray;">(Anda)</span>')
    tampil_user.short_description = 'User'

    def has_view_permission(self, request, obj=None):
        return obj.user == request.user if obj else request.user.is_authenticated

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return obj.user == request.user
        return True

admin.site.register(User, UserAdmin)
admin.site.register(Aktivitas, AktivitasAdmin)
admin.site.register(Kategori)
admin.site.register(Saran)
admin.site.register(Komen)
admin.site.register(Reply)
admin.site.register(Konten, KontenAdmin)
admin.site.register(Carousel)
admin.site.register(Konfigurasi, KonfigurasiAdmin)
admin.site.register(Galeri)