from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.timezone import localtime
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from admin_cms.models import User, Aktivitas, Kategori, Konfigurasi, Galeri, Komunitas, PeraturanKomunitas, Bookmarks
from user_cms.models import Konten, Saran, Komen, Balasan, Pertanyaan
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# UserAdmin
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'nama', 'email', 'level')
    # list_filter = ('is_active', 'is_staff', 'level', 'telepon')
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

# AktivitasAdmin
class AktivitasAdmin(admin.ModelAdmin):
    list_display = ('user', 'aksi', 'tanggal')
    # list_filter = ('user',)
    search_fields = ('user__username', 'aksi')
    ordering = ('-tanggal',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(user__is_superuser=True)

# KontenAdmin
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

# KonfigurasiAdmin
class KonfigurasiAdmin(admin.ModelAdmin):
    readonly_fields = ['tampil_user']

    fieldsets = (
        (None, {
            'fields': ('tampil_user',),
        }),
        ('Informasi Website', {
            'fields': ('judul_website', 'x', 'instagram', 'linkedin', 'facebook', 'tiktok', 'alamat', 'email', 'iklan', 'url_iklan')
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

# Komunitas Admin
class KomunitasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'status', 'jumlah_pertanyaan', 'tanggal', 'user')
    search_fields = ('nama',)
    readonly_fields = ['jumlah_pertanyaan']
    ordering = ('-tanggal',)

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

@admin.register(PeraturanKomunitas)
class PeraturanKomunitasAdmin(admin.ModelAdmin):
    list_display = ('komunitas','judul',)
    list_filter = ('komunitas',)

@admin.register(Bookmarks)
class BookmarksAdmin(admin.ModelAdmin):
    list_display = ('komunitas', 'judul', 'url_link')
    list_filter = ('komunitas',)

# Pertanyaan Admin
@admin.register(Pertanyaan)
class PertanyaanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'komunitas', 'created_at', 'penulis')
    ordering = ['created_at']

    def komunitas(self, obj):
        return obj.komunitas.nama
    komunitas.short_description = 'Komunitas'

admin.site.register(User, UserAdmin)
admin.site.register(Aktivitas, AktivitasAdmin)
admin.site.register(Kategori)
admin.site.register(Saran)
admin.site.register(Komen)
admin.site.register(Komunitas, KomunitasAdmin)
admin.site.register(Balasan)
admin.site.register(Konten, KontenAdmin)
admin.site.register(Konfigurasi, KonfigurasiAdmin)
admin.site.register(Galeri)
admin.site.unregister(Group)