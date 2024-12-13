from django.db import models
from admin_cms.models import User, Komunitas
from django.utils.text import slugify
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField

class Konten(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length=60)
    kategori = models.ForeignKey('admin_cms.Kategori', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255)
    isi_konten = RichTextField()
    tanggal = models.DateTimeField(auto_now_add=True)
    dilihat = models.PositiveIntegerField(default=0)
    username = models.CharField(max_length=60 , null=True , blank=True)
    foto = models.ImageField(upload_to="konten_foto/")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super(Konten, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Konten"
        verbose_name_plural = "Konten User"
        ordering = ['judul']

        permissions = [
            ("can_add_konten", "Can add konten"),
            ("can_change_konten", "Can change konten"),
            ("can_delete_konten", "Can delete konten"),
            ("can_view_konten", "Can view konten"),
        ]

    def __str__(self):
        return self.judul

class Pertanyaan(models.Model):
    komunitas = models.ForeignKey('admin_cms.Komunitas' , on_delete=models.CASCADE)
    judul = models.CharField(max_length=255)
    isi = models.TextField()
    penulis = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0, null=True,blank=True)

    class Meta:
        verbose_name = "Pertanyaan"
        verbose_name_plural = "Pertanyaan Komunitas"

    def __str__(self):
        return self.judul

class Jawaban(models.Model):
    pertanyaan = models.ForeignKey(Pertanyaan, related_name='jawaban_set', on_delete=models.CASCADE)
    isi = models.TextField()
    penulis = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Jawaban Pertanyaan"
        verbose_name_plural = "Jawaban Pertanyaan"

    def __str__(self):
        return f'Jawaban {self.penulis} - {self.pertanyaan.judul} - {self.isi}'

class Saran(models.Model):
    isi_saran = models.TextField()
    tanggal = models.DateTimeField(auto_now_add = True)
    nama = models.CharField(max_length=60)
    email = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Saran"
        verbose_name_plural = "Saran"

    def __str__(self):
        return self.isi_saran

class Komen(models.Model):
    konten = models.ForeignKey(Konten, related_name='komentar', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    email = models.EmailField()
    pesan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Komen"
        verbose_name_plural = "Komen User"

    def __str__(self):
        return f'{self.user.username} - {self.konten.judul}'

class Balasan(models.Model):
    komen = models.ForeignKey(Komen, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    email = models.EmailField()
    pesan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Balasan"
        verbose_name_plural = "Balasan User"
    
    reply_to = models.ForeignKey('self', null=True, blank=True, related_name='nested_replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.komen}"
