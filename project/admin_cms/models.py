from django.db import models
from admin_interface.models import Theme
from django.contrib.auth.models import AbstractUser, Permission
from admin_interface.models import Theme
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
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nama', 'level']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.level == 'Admin':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = True

        super(User, self).save(*args, **kwargs)

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

class Komunitas(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    nama = models.CharField(max_length=30)
    deskripsi = models.TextField()
    foto_komunitas = models.ImageField(upload_to="komunitas_foto/", blank=True, null=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    jumlah_pertanyaan = models.IntegerField(default=0, null=True, blank=True)

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

class PeraturanKomunitas(models.Model):
    komunitas = models.ForeignKey(Komunitas, on_delete=models.CASCADE)
    judul = models.CharField(max_length=60)
    deskripsi = models.TextField()

    class Meta:
        verbose_name = "Peraturan Komunitas"
        verbose_name_plural = "Peraturan Komunitas"

    def __str__(self):
        return f'{self.komunitas} - {self.judul}'

class Bookmarks(models.Model):
    komunitas = models.ForeignKey(Komunitas, on_delete=models.CASCADE)
    judul = models.CharField(max_length=155)
    url_link = models.URLField()

    class Meta:
        verbose_name = "Bookmark Komunitas"
        verbose_name_plural = "Bookmark Komunitas"
    
    def __str__(self):
        return f'{self.komunitas} - {self.judul}'

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
    foto = models.ImageField(upload_to='kategori_foto/')

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='konfigurasi')
    judul_website = models.CharField(max_length=100)
    instagram = models.CharField(max_length=50 , blank=True , null=True)
    facebook = models.CharField(max_length=50 , blank=True , null=True)
    x = models.CharField(max_length=50 , blank=True , null=True)
    linkedin = models.CharField(max_length=100 , blank=True , null=True)
    tiktok = models.CharField(max_length=50 , blank=True , null=True)
    alamat = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    iklan = models.ImageField(upload_to="gambar_iklan/", blank=True, null=True)
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
