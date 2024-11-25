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
    foto = models.ImageField(upload_to="user_foto/" , null=True , blank=True , default="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKsAAACUCAMAAADbGilTAAAAMFBMVEXk5ueutLenrrHg4+Tn6eqqsLTN0NLT1tjY29zGysy4vcC/xMbJzc/b3t/q7O2xt7pnBWjmAAAD/klEQVR4nO2cW7LbIAxADQiDIcD+d1ucx62TJr6AbIlMOR+dfp4qAiSQO02DwWAwGAwGg8FgMBicAQC3QQkxRmWNMTaoGHs2VmH2Qkqptc5/yuRNyDHmtvoXAHtxQost2dnPtreEgGhdehZ9+CYfIrfeE8G9Fb1H16luQgtqkZ9Vr7pLJ7ZgdoL6kHW2B1lYfhO9MfPLKv9rUH/ygFvVlZmusp45suWqqyynaUVUb7KMaeCrVNec5UqDuBQuqw2GRxasrFYVwrK4qtSgKhxLyhaeAS/oC0MW2PpkvSLpAwvvS8ACyI8EMK2qIpGXMXWnwHNgaU3BtKsKEWhla0+sLcRbQcCEVWjKBgzm5pW1IilPWkCsrBVPGFhoqQQ2JDrVqalq2UK3xUJpj/URukYxItNVCLqau60a3ELXzAS0K1kVCxarKhLVMYsrBm5QtTIwo1U1mesF7Sq/yFWb4XqGK10OfNPa+qY9C+9KdhZ80xmLr100nSug47pQqeZaG+tKV2sjLojuEF4TfVNviE1Y0p4bd5ehSV8NkHdEtJeaqLs32pcjXPlC/RaDWF3UT52YLZb8Pa5926J/7gbTeB4wvBm1bgV64Zgqsl/0xtmWBVQN7Aux4RqWb0Kn9h6Wc+SlsvHSjs00o6pcWVUnqGgT+ccK96Yen1U9t2qmTFbTta47wFyQB8n0MQQLwe+fClr7wP/7PzBiJxFk4hl0+gCAeZ8I+Z/gmObHPgOTWZLWr8PlbjG9zZavwBTWUfjryP51al/7i1U9zuzfyUG0Zs6YoHoM6AZYiSvXv/Upmw1zDoQ1psuNHNr1SxOIXSlff/fFpbc7QUo5a3v4mAdABTv7JPe+L1iXmcj7QWBcZxCVufi0dwpshXX2nQNLgPPu7+ubw+TmibgwAGX97u++E2Dp5kCWDNevnzTiAlYLb0hsP3/9VGWbc+Fs23zqo0UfXE691cimDjtF9hed5vOq2mjR71ovuMs5exioo01XzijDYcIPDbxFHt7e5pbqqCX1ij64b4gnBfXOgbdcOVOPW/3v0IeN8UPx1Uq77EF3nQdMD5bYHvE+d8DQUJks/tXrgFmsUlmHrBBO3gCeZXGRRb6918pi7pKpcvVHtj2yNDvAs2xjygJuoKGNxs961OlHwDvaioMzSsDfSQ3dAn4GqxFX35MrJlWh60sDngxYqZ03pd+uNtS+LqG/zkGgqwLLtrBuVC2viB5wRSEr2kVo/Vb7KCqOWuynj2gqtgL87DiWuTisxKXgG4qLw1Mug+oo3rbqBkPOcS09aNFfvx5A4Rbb8l+hHI4sdGXfBUTxhGTsIAWKx897cC1svLgP2BtFxyzMsgdcUVxVUD1Qojr43/gDTjs3mRf1UggAAAAASUVORK5CYII=")
    recent_login = models.DateTimeField(auto_now=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nama', 'level']
    
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

class Aktivitas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aksi = models.CharField(max_length=255)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.aksi} pada {self.tanggal}"

class Kategori(models.Model):
    kategori = models.CharField(max_length=60)
    foto = models.ImageField(upload_to='kategori_foto/')

    def __str__(self):
        return self.kategori


class KontenDilihat(models.Model):
    konten = models.ForeignKey('user_cms.Konten', related_name="dilihats", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('konten', 'user')

class Carousel(models.Model):
    judul = models.CharField(max_length=60)
    foto = models.ImageField(upload_to="carousel_foto/")

    def __str__(self):
        return self.judul

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
        unique_together = ('user',)

    def __str__(self):
        return self.judul_website

class Galeri(models.Model):
    judul = models.CharField(max_length=60)
    foto = models.ImageField(upload_to="galeri_foto/")
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul
