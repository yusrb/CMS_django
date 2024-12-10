import random
from django.shortcuts import redirect , render , get_object_or_404
from django.shortcuts import (
    render,
    redirect,
)
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.core.cache import cache
from django.core.paginator import Paginator
from urllib.parse import urlencode
from typing import Any
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)
from django.urls import reverse_lazy , reverse
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from .forms import CustomUserCreationForm, ReplyForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Q, Count
from admin_cms.models import (
    User,
    Galeri,
    Kategori,
    Konfigurasi,
    KontenDilihat,
    Komunitas,
    PeraturanKomunitas,
    Bookmarks,
    )
from user_cms.models import (
    Saran,
    Konten,
    Komen,
    Balasan,
    Pertanyaan,
    Jawaban,
)
from .forms import (
    LevelChoiceForm,
    CustomUserCreationForm,
    KonfigurasiForm,
    KomenForm,
    PertanyaanForm,
    JawabanForm,
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
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        return context

    def form_valid(self, form):
        user = form.get_user()

        login(self.request, user)
        self.request.session['level'] = user.level

        if user.level == 'admin':
            return redirect('user:konfigurasi')
        elif user.level == 'user':
            return redirect('user:konfigurasi')
        else:
            return redirect('user:konfigurasi')

class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('user:konten_list')

class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user/user_register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:konten_list')
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
        context["konfigurasi"] = Konfigurasi.objects.filter(user = self.request.user)
        context["konfigurasi_home"] = Konfigurasi.objects.filter(user_id=1).first()
        context["design_user"] = get_object_or_404(User, pk=1)
        context['search_input'] = search_input
        return context

class UserDetailView(DetailView):
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
        context['top_posts_user'] = Konten.objects.filter(user=self.get_object().pk).order_by('-dilihat')[:5].annotate(total_komentar=Count('komentar') + Count('komentar__replies'))
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5].annotate(total_komentar=Count('komentar') + Count('komentar__replies'))
        context["kategoris"] = Kategori.objects.all()
        # context["konfigurasis"] = Konfigurasi.objects.filter(user = self.request.user)
        context["design_user"] = get_object_or_404(User, pk=1)
        context["konfigurasi_home"] = Konfigurasi.objects.filter(user_id=1).first()
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['foto', 'nama', 'telepon', 'about']

    def get_success_url(self):
        return reverse_lazy('user:user_profil', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)

        konfigurasi = get_object_or_404(Konfigurasi, user=self.request.user)
        konfigurasi.alamat = self.request.POST.get('alamat', konfigurasi.alamat)

        konfigurasi.save()

        return response

class UserSosmedUpdate(View):
    def post(self, request, pk):
        konfigurasi = get_object_or_404(Konfigurasi, user=request.user)

        konfigurasi.instagram = request.POST.get('instagram', konfigurasi.instagram)
        konfigurasi.facebook = request.POST.get('facebook', konfigurasi.facebook)
        konfigurasi.x = request.POST.get('x', konfigurasi.x)
        konfigurasi.linkedin = request.POST.get('linkedin', konfigurasi.linkedin)
        konfigurasi.tiktok = request.POST.get('tiktok', konfigurasi.tiktok)
        konfigurasi.alamat = request.POST.get('alamat', konfigurasi.alamat)

        konfigurasi.save()
        return redirect('user:user_profil', pk=request.user.pk)

class KomunitasListView(ListView):
    model = Komunitas
    template_name = "user/Komunitas/komunitas_list.html"
    context_object_name = 'komunitas'

    def get_queryset(self):
        search_input = self.request.GET.get('q', '')

        if search_input:
            return Komunitas.objects.filter(
                Q(nama__icontains=search_input) | Q(deskripsi__icontains=search_input), status=True
            )
        else:
            return Komunitas.objects.filter(status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['judul'] = "Komunitas"
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context["kategoris"] = Kategori.objects.all()
        context["komunitass"] = Komunitas.objects.all()
        context["design_user"] = get_object_or_404(User, pk=1)

        search_input = self.request.GET.get('q', '')
        context['search_input'] = search_input

        return context
class KomunitasDetailView(DetailView):
    model = Komunitas
    template_name = "user/Komunitas/komunitas_detail.html"
    context_object_name = "komunitas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        komunitas = self.get_object()
        context["judul"] = komunitas.nama
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context["kategoris"] = Kategori.objects.all()
        context["design_user"] = get_object_or_404(User, pk=1)
        context['pertanyaan_list'] = komunitas.get_pertanyaan_terkait().order_by('-created_at')
        context["form"] = PertanyaanForm()
        context['peraturans'] = PeraturanKomunitas.objects.filter(komunitas = self.get_object().id)
        context['bookmarks'] = Bookmarks.objects.filter(komunitas = self.get_object().id)

        if self.request.user.is_authenticated:
            cache_key = f'komunitas_{komunitas.id}_users_online'
            users_online = cache.get(cache_key, [])
            if self.request.user.id not in users_online:
                users_online.append(self.request.user.id)
                cache.set(cache_key, users_online, timeout=60 * 5)

        users_online_count = len(cache.get(f'komunitas_{komunitas.id}_users_online', []))
        context["users_online"] = users_online_count

        return context

def KomunitasJoinView(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Anda perlu login terlebih dahulu untuk bergabung dengan komunitas.")
        return redirect('user:user_login')

    komunitas = get_object_or_404(Komunitas, pk=pk)

    if request.user in komunitas.members.all():
        messages.info(request, "Anda sudah bergabung dengan komunitas ini.")
        return redirect('user:komunitas_detail', pk=komunitas.pk)

    komunitas.members.add(request.user)
    messages.success(request, f"Anda berhasil bergabung dengan komunitas {komunitas.nama}. 🎉🎉")

    return redirect('user:komunitas_detail', pk=komunitas.pk)

def KomunitasKeluarView(request, pk):
    komunitas = get_object_or_404(Komunitas, pk=pk)

    if request.user in komunitas.members.all():
        komunitas.members.remove(request.user)

        messages.success(request, f"Anda berhasil keluar dari komunitas {komunitas.nama}.")
    else:
        messages.error(request, "Anda tidak terdaftar dalam komunitas ini.")

    return redirect('user:komunitas_detail', pk=komunitas.pk)

def PertanyaanCreateView(request, komunitas_id):
    komunitas = get_object_or_404(Komunitas, id=komunitas_id)

    if request.user not in komunitas.members.all():
        messages.error(request, "Hanya anggota komunitas yang bisa membuat pertanyaan.")
        return redirect('user:komunitas_detail', pk=komunitas.id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PertanyaanForm(request.POST)
            if form.is_valid():
                pertanyaan = form.save(commit=False)
                pertanyaan.komunitas = komunitas
                pertanyaan.penulis = request.user
                pertanyaan.save()

                url = reverse('user:komunitas_detail', kwargs={'pk': komunitas.id})
                query_params = urlencode({'scroll_to': f'pertanyaan-{pertanyaan.id}'})
                return redirect(f"{url}?{query_params}")

            else:
                print(form.errors)
        else:
            form = PertanyaanForm()
    else:
        messages.error(request, 'Anda harus login terlebih dahulu untuk membuat Pertanyaan di Komunitas')
        return redirect('user:user_login')

    context = {
        'form': form,
        'komunitas': komunitas,
        'pertanyaan_list': Pertanyaan.objects.filter(komunitas=komunitas),
    }

    return render(request, 'user/komunitas_detail.html', context)

def PertanyaanDeleteView(request, pertanyaan_id):
    pertanyaan = get_object_or_404(Pertanyaan, id=pertanyaan_id)

    if pertanyaan.penulis != request.user:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk menghapus pertanyaan ini.")

    pertanyaan.delete()
    url = reverse('user:komunitas_detail', kwargs={'pk': pertanyaan.komunitas.id})
    query_params = urlencode({'scroll_to': 'pertanyaan-list'})
    return redirect(f"{url}?{query_params}")

def PertanyaanUpdateView(request, pertanyaan_id):
    pertanyaan = get_object_or_404(Pertanyaan, id=pertanyaan_id)

    if pertanyaan.penulis != request.user:
        return HttpResponseForbidden("Anda tidak memiliki izin untuk mengedit pertanyaan ini.")

    if request.method == 'POST':
        form = PertanyaanForm(request.POST, instance=pertanyaan)
        if form.is_valid():
            form.save()
            url = reverse('user:komunitas_detail', kwargs={'pk': pertanyaan.komunitas.id})
            query_params = urlencode({'scroll_to': f'pertanyaan-{pertanyaan.id}'})
            return redirect(f"{url}?{query_params}")
    else:
        form = PertanyaanForm(instance=pertanyaan)

    context = {
        'form': form,
        'pertanyaan': pertanyaan,
        'komunitas': pertanyaan.komunitas,
    }

    return render(request, 'user/Komunitas/komunitas_detail.html', context)

def JawabanPertanyaanCreateView(request, pertanyaan_id):
    pertanyaan = get_object_or_404(Pertanyaan, id=pertanyaan_id)

    if request.user not in pertanyaan.komunitas.members.all():
        messages.error(request, "Hanya anggota komunitas yang bisa memberikan jawaban.")
        return redirect('user:komunitas_detail', pk=pertanyaan.komunitas.id)

    if request.user.is_authenticated:
        if request.method == "POST":
            jawaban_isi = request.POST.get('isi')

            penulis = request.user

            jawaban = pertanyaan.jawaban_set.create(isi=jawaban_isi, penulis=penulis)

            url = reverse('user:komunitas_detail', kwargs={'pk': pertanyaan.komunitas.id})
            query_params = urlencode({'scroll_to': f'pertanyaan-{pertanyaan.id}'})

            full_url = f'{url}?{query_params}'

            return redirect(full_url)
    else:
        messages.error(request, 'Anda harus login terlebih dahulu untuk membuat jawaban')
        return redirect('user:user_login')

    return render(request, 'user_cms/jawab_pertanyaan.html', {'pertanyaan': pertanyaan})

def JawabanPertanyaanDeleteView(request, pertanyaan_id, jawaban_id):
    pertanyaan = get_object_or_404(Pertanyaan, id=pertanyaan_id)
    jawaban = get_object_or_404(Jawaban, id=jawaban_id, pertanyaan=pertanyaan)

    if jawaban.penulis == request.user:
            jawaban.delete()

    url = reverse('user:komunitas_detail', kwargs={'pk': pertanyaan.komunitas.id})
    query_params = urlencode({'scroll_to': f'pertanyaan-{pertanyaan.id}'})
    full_url = f'{url}?{query_params}'
    return redirect(full_url)

def JawabanPertanyaanUpdateView(request, pertanyaan_id):
    pertanyaan = get_object_or_404(Pertanyaan, id=pertanyaan_id)

    if request.method == "POST":
        jawaban.delete()

        url = reverse('user:komunitas_detail', kwargs={'pk': pertanyaan.komunitas.id})
        query_params = urlencode({'scroll_to': f'pertanyaan-{pertanyaan.id}'})

        full_url = f'{url}?{query_params}'

        return redirect(full_url)

    return render(request, 'user_cms/jawab_pertanyaan.html', {'pertanyaan': pertanyaan})

def JawabanPertanyaanUpdateView(request, pertanyaan_id, jawaban_id):
    pertanyaan = get_object_or_404(Pertanyaan, id=pertanyaan_id)
    jawaban = get_object_or_404(Jawaban, id=jawaban_id, pertanyaan=pertanyaan)

    if request.method == 'POST':
        jawaban_isi = request.POST.get('isi')
        jawaban.isi = jawaban_isi
        jawaban.save()

        url = reverse('user:komunitas_detail', kwargs={'pk': pertanyaan.komunitas.id})
        query_params = urlencode({'scroll_to': f'pertanyaan-{pertanyaan.id}'})

        full_url = f'{url}?{query_params}'

        return redirect(full_url)

    return render(request, 'user/update_jawaban.html', {'jawaban': jawaban, 'pertanyaan': pertanyaan})

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
        # context["konfigurasis"] = Konfigurasi.objects.filter(user = self.request.user)
        context["design_user"] = get_object_or_404(User, pk=1)
        return context

class KontenListView(ListView):
    model = Konten
    template_name = 'user/konten_list.html'
    context_object_name = 'kontens'
    paginate_by = 6

    # def get(self, request, *args, **kwargs):
    #     konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

    #     if not konfigurasi or not konfigurasi.alamat:
    #         return redirect('user:konfigurasi')

    #     return super().get(request, *args, **kwargs)

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
        # context['konfigurasis'] = Konfigurasi.objects.filter(user=self.request.user)
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context['galeris'] = Galeri.objects.all()
        context['search_input'] = search_input
        context["design_user"] = get_object_or_404(User, pk=1)

        return context

class KontenLatestListView(ListView):
    model = Konten
    template_name = 'user/konten_latest.html'
    context_object_name = 'kontens'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_theme_config = User.objects.filter(username=self.request.user.username).first()

        if user_theme_config:
            context['theme'] = user_theme_config.theme

        search_input = self.request.GET.get('q')
        
        if search_input:
            kontens = Konten.objects.filter(judul__icontains=search_input).annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            ).distinct()
        else:
            kontens = Konten.objects.all().annotate(
                total_komentar=Count('komentar') + Count('komentar__replies')
            )

        # Paginasi
        paginator = Paginator(kontens, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['kontens'] = page_obj
        context['page_obj'] = page_obj
        context["judul"] = 'Daftar Konten Latest'
        context['top_posts'] = Konten.objects.order_by('-dilihat')[:5]
        context["kategoris"] = Kategori.objects.all()
        context["konfigurasis"] = Konfigurasi.objects.filter(user=self.request.user)
        context["konfigurasi_home"] = Konfigurasi.objects.filter(user_id=1).first()
        context["design_user"] = get_object_or_404(User, username=self.request.user.username)

        return context
        
class KontenTanggalListView(ListView):
    model = Konten
    template_name = 'user/konten_tanggal_list.html'
    context_object_name = 'kontens'

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

class KategoriListView(ListView):
    model = Kategori
    template_name = 'user/kategori_list.html'
    context_object_name = 'kategoris'

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
        context['konfigurasi_home'] = Konfigurasi.objects.filter(user_id=1).first()
        context["design_user"] = get_object_or_404(User, pk=1)
        context['search_input'] = search_input

        return context

class KategoriDetailView(DetailView):
    model = Kategori
    template_name = 'user/kategori_detail.html'
    context_object_name = 'kategori'

    # def get(self, request, *args, **kwargs):
    #     konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

    #     if not konfigurasi or not konfigurasi.alamat:
    #         return redirect('user:konfigurasi')

    #     return super().get(request, *args, **kwargs)

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
        context['search_input'] = search_input
        return context
        
class KontenDetailView(DetailView):
    model = Konten
    template_name = 'user/konten_detail.html'
    context_object_name = 'konten'

    def get(self, request, *args, **kwargs):
        # konfigurasi = Konfigurasi.objects.filter(user=self.request.user).first()

        # if not konfigurasi or not konfigurasi.alamat:
        #     return redirect('user:konfigurasi')

        konten = self.get_object()

        if request.user.is_authenticated:
            if not KontenDilihat.objects.filter(konten=konten, user=request.user).exists():
                konten.dilihat += 1
                konten.save()

                KontenDilihat.objects.create(konten=konten, user=request.user)
    
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        komentar_queryset = Komen.objects.filter(konten=self.get_object())
        total_komentar = komentar_queryset.count()
        total_balasan = Balasan.objects.filter(komen__in=komentar_queryset).count()
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
        if request.user.is_authenticated:
            self.object = self.get_object()
            form = KomenForm(request.POST)

            if form.is_valid():
                komen = form.save(commit=False)
                komen.konten = self.object
                komen.user = request.user
                komen.save()
                return redirect('user:konten_detail', slug=self.object.slug)
        else:
            messages.error(request, 'Anda harus login untuk memberikan komentar.')
            return redirect('user:user_login')

        return self.get(request, *args, **kwargs)

class ReplyKomenView(LoginRequiredMixin, View):
    def post(self, request, komen_id):
        parent_komen = get_object_or_404(Komen, id=komen_id)
        konten = parent_komen.konten

        Balasan.objects.create(
            user=request.user,
            komen=parent_komen,
            nama=request.POST.get('nama'),
            email=request.POST.get('email'),
            pesan=request.POST.get('pesan')
        )

        return redirect(f"{reverse('user:konten_detail', kwargs={'slug': konten.slug})}?hash=#komen-{parent_komen.id}")

class ReplyUpdateView(View):
    def post(self, request, reply_id):
        reply = get_object_or_404(Balasan, pk=reply_id)
        parent_komen = reply.komen
        konten = parent_komen.konten

        if request.user != reply.user:
            return redirect(reverse('user:konten_detail', kwargs={'slug': konten.slug}) + '?hash=#komen-error')

        reply.pesan = request.POST.get('pesan')
        reply.save()

        return redirect(f"{reverse('user:konten_detail', kwargs={'slug': konten.slug})}?hash=#comments-section")

class ReplyDeleteView(View):
    def post(self, request, reply_id):
        reply = get_object_or_404(Balasan, pk=reply_id)
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

        Balasan.objects.filter(komen=komen).delete()

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
        konfigurasi = Konfigurasi.objects.filter(user=request.user).first()

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
