import os
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.timezone import timezone

class User(AbstractUser):
    LEVEL_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )

    username = models.CharField(max_length=60, unique=True)
    nama = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    about = models.CharField(max_length=100 , null=True, blank=True)
    telepon = models.CharField(max_length=20)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='User')
    foto = models.ImageField(upload_to="user_foto/" , null=True , blank=True)
    recent_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nama', 'level']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    def __str__(self):
        return self.username

    
    def save(self, *args, **kwargs):
        try:
            old_instance = User.objects.get(pk=self.pk)
            if old_instance.foto and old_instance.foto != self.foto:
                if os.path.isfile(old_instance.foto.path):
                    os.remove(old_instance.foto.path)
        except User.DoesNotExist:
            pass

        # Set is_superuser dan is_staff berdasarkan level
        if self.level == 'Admin':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = True

        super(User, self).save(*args, **kwargs)

        # Tambahkan izin untuk level User
        if self.level == 'User':
            permissions = [
                'can_add_konten',
                'can_change_konten',
                'can_delete_konten',
                'can_view_konten'
            ]

            for perm in permissions:
                permission = Permission.objects.get(codename=perm)
                self.user_permissions.add(permission)

class PeraturanKomunitas(models.Model):
    komunitas = models.ForeignKey('Komunitas', on_delete=models.CASCADE, related_name='peraturan_komunitas')
    judul = models.CharField(max_length=60)
    deskripsi = models.TextField()

    class Meta:
        verbose_name = "Peraturan Komunitas"
        verbose_name_plural = "Peraturan Komunitas"

    def __str__(self):
        return f'{self.komunitas.nama} - {self.judul}'

class Bookmarks(models.Model):
    komunitas = models.ForeignKey('Komunitas', on_delete=models.CASCADE, related_name='bookmarks')
    judul = models.CharField(max_length=155)
    url_link = models.URLField()

    class Meta:
        verbose_name = "Bookmark Komunitas"
        verbose_name_plural = "Bookmark Komunitas"

    def __str__(self):
        return f'{self.komunitas.nama} - {self.judul}'

class Komunitas(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=True, blank=True)
    nama = models.CharField(max_length=30, null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    foto_komunitas = models.ImageField(upload_to="komunitas_foto/", null=True, blank=True)
    tanggal = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    peraturan = models.ManyToManyField('PeraturanKomunitas', related_name='komunitas_peraturan', blank=True)
    boomark = models.ManyToManyField('Bookmarks', related_name='komunitas_bookmarks', blank=True)

    status = models.BooleanField(default=True, null=True, blank=True)
    jumlah_pertanyaan = models.IntegerField(default=0, null=True, blank=True)
    
    members = models.ManyToManyField(User, related_name='komunitas_members', blank=True)

    class Meta:
        verbose_name = "Komunitas"
        verbose_name_plural = "Komunitas"

    def update_pertanyaan_count(self):
        self.jumlah_pertanyaan = self.pertanyaan_set.count()
        self.save()

    def get_pertanyaan_terkait(self):
        return self.pertanyaan_set.all()

    def __str__(self):
        return self.nama

class Aktivitas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aksi = models.CharField(max_length=255)
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aktivitas"
        verbose_name_plural = "Aktivitas User"

    def __str__(self):
        formatted_date = self.tanggal.strftime('%d %B %Y')
        return f"{self.user.username} - {self.aksi} pada {formatted_date}"


class Kategori(models.Model):
    kategori = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"

    def __str__(self):
        return self.kategori


class KontenDilihat(models.Model):
    konten = models.ForeignKey('user_cms.Konten', related_name="dilihats", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Konten Dilihat"
        verbose_name_plural = "Konten Dilihat"
        unique_together = ('konten', 'user')

class Konfigurasi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='konfigurasi' , default=1)
    judul_website = models.CharField(max_length=100)
    favicon = models.ImageField(upload_to="favicon_foto/", null=True)

    instagram = models.CharField(max_length=50 , blank=True , null=True)
    facebook = models.CharField(max_length=50 , blank=True , null=True)
    x = models.CharField(max_length=50 , blank=True , null=True)
    linkedin = models.CharField(max_length=100 , blank=True , null=True)
    tiktok = models.CharField(max_length=50 , blank=True , null=True)
    alamat = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    iklan = models.ImageField(upload_to="gambar_iklan/", blank=True, null=True, help_text="Masukkan Gambar yang telah disepakati")
    url_iklan = models.CharField(max_length=100, blank=True, null=True , help_text="Masukkan Url iklan yang telah disepakati ('opsional')")

    class Meta:
        verbose_name = "Konfigurasi Admin"
        verbose_name_plural = "Konfigurasi Admin"
        unique_together = ('user',)

    def __str__(self):
        return self.judul_website

class Galeri(models.Model):
    judul = models.CharField(max_length=60)
    foto = models.ImageField(upload_to="galeri_foto/")
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Galeri"
        verbose_name_plural = "Galeri"

    def __str__(self):
        return self.judul
