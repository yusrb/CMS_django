import random
from typing import Any
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView , DeleteView
from django.urls import reverse_lazy , reverse
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from .forms import CustomUserCreationForm, ReplyForm
from django.shortcuts import redirect , render , get_object_or_404
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from .models import Saran
from django.db.models import Q, Count
from admin_cms.models import (
    User,
    Galeri,
    Kategori,
    Konfigurasi,
    KontenDilihat,
    Komunitas,
    )
from user_cms.models import (
    Konten,
    Komen,
    Balasan,
    Pertanyaan,
)
from .forms import (
    LevelChoiceForm,
    CustomUserCreationForm,
    KonfigurasiForm,
    KomenForm
    )

class UserLoginView(LoginView):
    template_name = 'user/user_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:konten_list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judul'] = 'Login Page'
        context['level_form'] = LevelChoiceForm()
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context

    def form_valid(self, form):
        selectTerpilih = self.request.POST.get('level')

        user = form.get_user()

        if selectTerpilih != user.level:
            messages.error(self.request, f"Level '{selectTerpilih}' tidak sesuai dengan akun Anda.")
            return self.form_invalid(form)

        login(self.request, user)
        self.request.session['level'] = selectTerpilih
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('user:konfigurasi')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('user:konten_list')

class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user/user_register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            form.add_error('password2', "Passwords do not match")
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.level = 'User'
        user.save()

        konfigurasi = Konfigurasi.objects.create(
            user=user,
            judul_website='Aspire CMS',
            email=user.email,
        )

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["judul"] = "Register Page" 
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('user:user_login')

class UserProfilView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_profil.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

        if not konfigurasi or not konfigurasi.alamat:
            return redirect('user:konfigurasi')

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('q')

        if search_input:
            context['kontens'] = Konten.objects.filter(
                user = self.request.user,
                judul__icontains=search_input
            ).annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            ).distinct()
        else:
            context['kontens'] = Konten.objects.filter(
                user=self.request.user,
            ).order_by('-tanggal').annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            )

        context["judul"] = 'Profil User'
        context['top_posts'] = Konten.objects.filter(user=self.get_object().pk).order_by('-dilihat')[:5].annotate(total_komentar=Count('komentar') + Count('komentar__replies'))
        context["kategoris"] = Kategori.objects.all()
        context["konfigurasis"] = Konfigurasi.objects.filter(user = self.request.user)
        context["konfigurasi_home"] = Konfigurasi.objects.filter(user_id=1).first()
        context["design_user"] = get_object_or_404(User, pk=1)
        context['search_input'] = search_input
        return context

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_id = kwargs.get('pk')

        if user.id != int(user_id):
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('user:user_profil' , kwargs={'pk' : user.id}))

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('q')

        if search_input:
            context['kontens'] = Konten.objects.filter(
                user=self.get_object().pk ,
                judul__icontains=search_input
            ).annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            ).distinct()
        else:
            context['kontens'] = Konten.objects.filter(
                user=self.get_object().pk,
            ).order_by('-tanggal').annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            )

        context["judul"] = 'Detail User'
        context['top_posts_user'] = Konten.objects.filter(user=self.get_object().pk).order_by('-dilihat')[:5]
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5].annotate(total_komentar=Count('komentar') + Count('komentar__replies'))
        context["kategoris"] = Kategori.objects.all()
        context["konfigurasis"] = Konfigurasi.objects.filter(user = self.request.user)
        context["design_user"] = get_object_or_404(User, pk=1)
        context["konfigurasi_home"] = Konfigurasi.objects.filter(user_id=1).first()
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['foto', 'nama', 'telepon', 'about']

    def get_success_url(self):
        return reverse_lazy('user:user_profil', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)

class UserSosmedUpdate(View):
    def post(self, request, pk):
        konfigurasi = get_object_or_404(Konfigurasi, user=request.user)

        konfigurasi.instagram = request.POST.get('instagram', konfigurasi.instagram)
        konfigurasi.facebook = request.POST.get('facebook', konfigurasi.facebook)
        konfigurasi.x = request.POST.get('x', konfigurasi.x)
        konfigurasi.linkedin = request.POST.get('linkedin', konfigurasi.linkedin)
        konfigurasi.tiktok = request.POST.get('tiktok', konfigurasi.tiktok)

        konfigurasi.save()
        return redirect('user:user_profil', pk=request.user.pk)

class KomunitasListView(ListView):
    model = Komunitas
    template_name = "user/Komunitas/komunitas_list.html"
    context_object_name = 'komunitas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judul'] = "Komunitas"
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context["kategoris"] = Kategori.objects.all()
        context["konfigurasis"] = Konfigurasi.objects.filter(user = self.request.user)
        context["design_user"] = get_object_or_404(User, pk=1)
        return context

class ContactView(ListView):
    model = Konfigurasi
    template_name = 'user/contact.html'
    context_object_name = 'konfigurasi'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["judul"] = 'Contact Page'
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context["kategoris"] = Kategori.objects.all()
        context["konfigurasis"] = Konfigurasi.objects.filter(user = self.request.user)
        context["design_user"] = get_object_or_404(User, pk=1)
        return context

class KontenListView(LoginRequiredMixin, ListView):
    model = Konten
    template_name = 'user/konten_list.html'
    context_object_name = 'kontens'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

        if not konfigurasi or not konfigurasi.alamat:
            return redirect('user:konfigurasi')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        get_konten = Konten.objects.annotate(
            total_komentar=Count('komentar') + Count('komentar__replies')
        )

        konten_random = random.sample(list(get_konten), min(len(get_konten), 6))

        search_input = self.request.GET.get('q')

        if search_input:
            konten_random_carousel = Konten.objects.filter(
                Q(judul__icontains=search_input)
            ).annotate(total_komentar=Count('komentar')).distinct()
        else:
            konten_random_carousel = random.sample(list(get_konten), min(len(get_konten), 6))

        context["judul"] = "Daftar Konten"
        context['kontens_random_carousel'] = konten_random_carousel
        context['kontens_random'] = konten_random
        context['kategoris'] = Kategori.objects.all()
        context['post_terbarus'] = Konten.objects.filter(
            tanggal__lte=timezone.now()
        ).order_by('-tanggal')[:4].annotate(total_komentar=Count("komentar") + Count("komentar__replies"))
        context['top_posts'] = Konten.objects.order_by('-dilihat').annotate(total_komentar=Count("komentar"))[:5]
        context['konfigurasis'] = Konfigurasi.objects.filter(user=self.request.user)
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context['galeris'] = Galeri.objects.all()
        context['search_input'] = search_input
        context["design_user"] = get_object_or_404(User, pk=1)

        return context

class KontenLatestListView(LoginRequiredMixin, ListView):
    model = Konten
    template_name = 'user/konten_latest.html'
    context_object_name = 'kontens'

    def get(self, request, *args, **kwargs):
        if not hasattr(request.user, 'konfigurasi'):
            return redirect('user:konfigurasi')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_theme_config = User.objects.filter(username=self.request.user.username).first()
        
        if user_theme_config:
            context['theme'] = user_theme_config.theme

        search_input = self.request.GET.get('q')

        if search_input:
            context['kontens'] = Konten.objects.filter(
                judul__icontains=search_input
            ).annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            ).distinct()
        else:
            context['kontens'] = Konten.objects.order_by('-tanggal').annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            )

        context["judul"] = 'Daftar Konten Latest'
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context["kategoris"] = Kategori.objects.all()
        context["konfigurasis"] = Konfigurasi.objects.filter(user=self.request.user)
        context["konfigurasi_home"] = Konfigurasi.objects.filter(user_id=1).first()
        context["design_user"] = get_object_or_404(User, pk=1)
        context['search_input'] = search_input
        return context

class KontenTanggalListView(LoginRequiredMixin, ListView):
    model = Konten
    template_name = 'user/konten_tanggal_list.html'
    context_object_name = 'kontens'

    def get(self, request, *args, **kwargs):
        if not hasattr(request.user, 'konfigurasi'):
            return redirect('user:konfigurasi')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('q')

        if search_input:
            kontens = Konten.objects.filter(
                judul__icontains=search_input
            ).annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            ).distinct()
        else:
            kontens = Konten.objects.order_by('-tanggal').annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            )

        konten_grouped = {}
        for konten in kontens:
            konten_date = konten.tanggal.date()

            konten_date = konten_date.replace(day=konten_date.day + 1)  

            if konten_date not in konten_grouped:
                konten_grouped[konten_date] = []
            konten_grouped[konten_date].append(konten)

        context['konten_grouped'] = konten_grouped
        context['search_input'] = search_input
        context["design_user"] = get_object_or_404(User, pk=1)
        context['kategoris'] = Kategori.objects.all()
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context["judul"] = 'Daftar Konten Berdasarkan Tanggal'
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()

        return context

class KategoriListView(LoginRequiredMixin, ListView):
    model = Kategori
    template_name = 'user/kategori_list.html'
    context_object_name = 'kategoris'

    def get(self, request, *args, **kwargs):
        if not hasattr(request.user, 'konfigurasi'):
            return redirect('user:konfigurasi')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('q')

        if search_input:
            context['kategoris'] = Kategori.objects.filter(
                Q(kategori__icontains=search_input) |
                Q(konten__judul__icontains=search_input)
            ).distinct()

            context['kontens_with_comments'] = Konten.objects.filter(
                judul__icontains=search_input
            ).annotate(total_komentar=Count('komentar') + Count('komentar__replies'))
        else:
            context['kategoris'] = Kategori.objects.all()

        for kategori in context["kategoris"]:
            kategori.kontens_with_comments = kategori.konten_set.annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            ).order_by('-tanggal')[:4]

        context["judul"] = 'Daftar Kategori'
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context["konfigurasis"] = Konfigurasi.objects.filter(user=self.request.user)
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context["design_user"] = get_object_or_404(User, pk=1)
        context['search_input'] = search_input

        return context

class KategoriDetailView(LoginRequiredMixin, DetailView):
    model = Kategori
    template_name = 'user/kategori_detail.html'
    context_object_name = 'kategori'

    def get(self, request, *args, **kwargs):
        konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

        if not konfigurasi or not konfigurasi.alamat:
            return redirect('user:konfigurasi')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('q')

        kategori_obj = self.get_object()

        if search_input:
            context['kontens'] = Konten.objects.filter(
                judul__icontains=search_input
            ).annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            ).distinct()
        else:
            context['kontens'] = Konten.objects.order_by('-tanggal').annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            )

        context["judul"] = kategori_obj.kategori
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context["kategoris"] = Kategori.objects.all()
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context["design_user"] = get_object_or_404(User, pk=1)
        context["konfigurasis"] = Konfigurasi.objects.filter(user=self.request.user)
        context['search_input'] = search_input
        return context
        
class KontenDetailView(LoginRequiredMixin,DetailView):
    model = Konten
    template_name = 'user/konten_detail.html'
    context_object_name = 'konten'

    def get(self, request, *args, **kwargs):
        konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

        if not konfigurasi or not konfigurasi.alamat:
            return redirect('user:konfigurasi')

        konten = self.get_object()

        if not KontenDilihat.objects.filter(konten=konten, user=request.user).exists():
            konten.dilihat += 1
            konten.save()

            KontenDilihat.objects.create(konten=konten, user=request.user)
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        komentar_queryset = Komen.objects.filter(konten=self.get_object())
        total_komentar = komentar_queryset.count()
        total_balasan = Reply.objects.filter(komen__in=komentar_queryset).count()
        total_komentar += total_balasan

        context["judul"] = self.get_object().judul
        context['kontens'] = Konten.objects.all()
        context['kategoris'] = Kategori.objects.all()
        context["konten_lain"] = Konten.objects.filter(kategori=self.object.kategori).exclude(id=self.object.id).order_by('-tanggal')[:2]
        context["komentars"] = total_komentar
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context['konfigurasis'] = Konfigurasi.objects.filter(user_id=self.request.user.pk)
        context["design_user"] = get_object_or_404(User, pk=1)
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()

        context['komentar'] = self.object.komentar.all()
        context['komen_form'] = KomenForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = KomenForm(request.POST)

        if form.is_valid():
            komen = form.save(commit=False)
            komen.konten = self.object
            komen.user = request.user
            komen.save()
            return redirect('user:konten_detail', slug=self.object.slug)

        return self.get(request, *args, **kwargs)

class ReplyKomenView(View):
    def post(self, request, komen_id):
        parent_komen = get_object_or_404(Komen, id=komen_id)
        konten = parent_komen.konten 

        Reply.objects.create(
            user=request.user,
            komen=parent_komen,
            nama=request.POST.get('nama'),
            email=request.POST.get('email'),
            pesan=request.POST.get('pesan')
        )

        return redirect(f"{reverse('user:konten_detail', kwargs={'slug': konten.slug})}?hash=#komen-{parent_komen.id}")

class ReplyUpdateView(View):
    def post(self, request, reply_id):
        reply = get_object_or_404(Reply, pk=reply_id)
        parent_komen = reply.komen
        konten = parent_komen.konten

        if request.user != reply.user:
            return redirect(reverse('user:konten_detail', kwargs={'slug': konten.slug}) + '?hash=#komen-error')

        reply.pesan = request.POST.get('pesan')
        reply.save()

        return redirect(f"{reverse('user:konten_detail', kwargs={'slug': konten.slug})}?hash=#comments-section")

class ReplyDeleteView(View):
    def post(self, request, reply_id):
        reply = get_object_or_404(Reply, pk=reply_id)
        parent_komen = reply.komen
        konten = parent_komen.konten

        if request.user != reply.user:
            return redirect(reverse('user:konten_detail', kwargs={'slug': konten.slug}) + '?hash=#komen-error')

        reply.delete()

        return redirect(f"{reverse('user:konten_detail', kwargs={'slug': konten.slug})}?hash=#comments-section")

class KomentarUpdateView(View):
    def post(self, request, komen_id):
        parent_komen = get_object_or_404(Komen, id=komen_id)
        konten = parent_komen.konten

        if request.user != parent_komen.user:
            return redirect(reverse('user:konten_detail', kwargs={'slug': konten.slug}) + '?hash=#komen-error')

        parent_komen.pesan = request.POST.get('pesan')
        parent_komen.save()

        return redirect(f"{reverse('user:konten_detail', kwargs={'slug': konten.slug})}?hash=#komen-{parent_komen.id}")

class KomentarDeleteView(View):
    def post(self, request, komen_id):
        komen = get_object_or_404(Komen, pk=komen_id)
        konten = komen.konten

        Reply.objects.filter(komen=komen).delete()

        komen.delete()

        return redirect(reverse('user:konten_detail', kwargs={'slug': konten.slug}) + "?hash=#comments-section")

class GaleriListView(ListView):
    model = Galeri
    template_name = 'user/galeri_list.html'
    context_object_name = 'galeris'

class SaranCreateView(CreateView):
    model = Saran
    fields = ['isi_saran', 'nama', 'email']
    template_name = 'user/saran_form.html'

    def form_valid(self, form):
        saran_instance = form.save()

        send_mail(
            'Saran Baru Diterima',
            f'''
            Nama Pengirim: {saran_instance.nama}
            Email Pengirim: {saran_instance.email}
            Isi Saran:
            {saran_instance.isi_saran}
            ''',
            saran_instance.email,
            ['byrn.uiy@gmail.com'],
            fail_silently=False,
            html_message=f'''
            <html>
                <body>
                    <div style="padding-left: 0px;">
                        <p><strong>Nama Pengirim:</strong> {saran_instance.nama}</p>
                        <p><strong>Email Pengirim:</strong> {saran_instance.email}</p>
                        <p style="margin-bottom:0px"><strong>Isi Saran:</strong>
                        {saran_instance.isi_saran}
                        </p>
                    </div>
                </body>
            </html>
            '''
        )

        messages.success(self.request, 'Terimakasih atas saran Anda!')

        return super().form_valid(form)

    def get_success_url(self):
        asal = self.request.GET.get('asal', 'konten_list')
        slug = self.request.GET.get('slug', '')
        pk = self.request.GET.get('pk', '')

        if asal == 'konten_latest':
            return f"{reverse('user:konten_latest')}?scroll_to=saran_form"
        elif asal == 'kontens_by_date':
            return f"{reverse('user:konten_tanggal_list')}?scroll_to=saran_form"
        elif asal == 'kategori_list':
            return f"{reverse('user:kategori_list')}?scroll_to=saran_form"
        elif asal == 'contact':
            return f"{reverse('user:contact')}?scroll_to=saran_form"
        elif asal == 'konten_detail' and slug:
            return f"{reverse('user:konten_detail', kwargs={'slug': slug})}?scroll_to=saran_form"
        elif asal == 'kategori_detail' and pk:
            return f"{reverse('user:kategori_detail' , kwargs={'pk': pk})}?scroll_to=saran_form"
        elif asal == 'saran_form':
            return f"{reverse('user:konten_list')}?scroll_to=saran_form"
        else:
            return f"{reverse('user:konten_list')}?scroll_to=saran_form"

class KonfigurasiUpdateView(UpdateView):
    model = Konfigurasi
    form_class = KonfigurasiForm
    template_name = 'user/konfigurasi.html'

    def get(self, request, *args, **kwargs):
        konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

        if konfigurasi and konfigurasi.alamat:
            return redirect('user:konten_list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["judul"] = "Konfigurasi Page"
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context

    def get_object(self):
        konfigurasi, created = Konfigurasi.objects.get_or_create(user=self.request.user)
        return konfigurasi

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user:konten_list')