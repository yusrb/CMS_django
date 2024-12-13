from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.timezone import localtime
from django.utils.html import format_html
from admin_cms.models import User, Aktivitas, Kategori, Konfigurasi, Galeri, Komunitas, PeraturanKomunitas, Bookmarks
from user_cms.models import Konten, Saran, Komen, Balasan, Pertanyaan, Jawaban

# ===============================
# User Admin
# ===============================

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'nama', 'email', 'level')
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
        return qs if request.user.is_superuser or request.user.is_staff else qs.filter(id=request.user.id)

# ===============================
# Aktivitas Admin
# ===============================

class AktivitasAdmin(admin.ModelAdmin):
    list_display = ('user', 'aksi', 'tanggal')
    search_fields = ('user__username', 'aksi')
    ordering = ('-tanggal',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.exclude(user__is_superuser=True)

# ===============================
# Konten Admin
# ===============================

class KontenAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'formatted_tanggal','user')
    search_fields = ('judul',)
    exclude = ('username', 'user', 'slug', 'dilihat')

    def formatted_tanggal(self, obj):
        return localtime(obj.tanggal).strftime('%d %b %Y, %H:%M WIB')
    formatted_tanggal.short_description = 'Tanggal'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
            obj.username = request.user.username
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.user == request.user or request.user.is_superuser
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.user == request.user or request.user.is_superuser
        return True

    def has_view_permission(self, request, obj=None):
        if obj:
            return obj.user == request.user or request.user.is_superuser
        return True

# ===============================
# Konfigurasi Admin
# ===============================

class KonfigurasiAdmin(admin.ModelAdmin):
    list_display = ('judul_website', 'email', 'alamat', 'user')
    readonly_fields = ['tampil_user']

    fieldsets = (
        (None, {
            'fields': ('tampil_user',),
        }),
        ('Informasi Website', {
            'fields': ('judul_website', 'favicon' , 'x', 'instagram', 'linkedin', 'facebook', 'tiktok', 'alamat', 'email', 'iklan', 'url_iklan')
        }),
    )

    def tampil_user(self, obj):
        return format_html(f'{obj.user} <span style="color: gray;">(Anda)</span>')
    tampil_user.short_description = 'User'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def has_view_permission(self, request, obj=None):
        return obj.user == request.user if obj else request.user.is_authenticated

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.user == request.user
        return True

# ===============================
# PeraturanKomunitas Inline
# ===============================

class PeraturanKomunitasInline(admin.TabularInline):
    model = Komunitas.peraturan.through
    extra = 1

class BookmarksInline(admin.TabularInline):
    model = Komunitas.boomark.through
    extra = 1

# ===============================
# Komunitas Admin
# ===============================

class KomunitasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'status', 'jumlah_pertanyaan', 'tanggal', 'user')
    search_fields = ('nama',)
    readonly_fields = ['jumlah_pertanyaan']
    ordering = ('-tanggal',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.user == request.user or request.user.is_superuser
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.user == request.user or request.user.is_superuser
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        if obj:
            return obj.user == request.user or request.user.is_superuser
        return request.user.is_superuser

# ===============================
# Pertanyaan Admin
# ===============================

@admin.register(Pertanyaan)
class PertanyaanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'komunitas', 'penulis')
    ordering = ['created_at']

    def komunitas(self, obj):
        return obj.komunitas.nama
    komunitas.short_description = 'Komunitas'

# ===============================
# Register Semua Model
# ===============================

admin.site.register(User, UserAdmin)
admin.site.register(Aktivitas, AktivitasAdmin)
admin.site.register(PeraturanKomunitas)
admin.site.register(Bookmarks)
admin.site.register(Kategori)
admin.site.register(Saran)
admin.site.register(Komen)
admin.site.register(Komunitas, KomunitasAdmin)
admin.site.register(Balasan)
admin.site.register(Konten, KontenAdmin)
admin.site.register(Konfigurasi, KonfigurasiAdmin)
admin.site.register(Galeri)
admin.site.register(Jawaban)

admin.site.unregister(Group)
