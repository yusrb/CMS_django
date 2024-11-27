from django.urls import path
from .views import (
    UserLoginView,
    UserRegisterView,
    UserLogoutView,
    UserProfilView,
    UserUpdateView,
    UserSosmedUpdate,
    UserDetailView,

    KomunitasListView,

    KontenListView,
    KontenLatestListView,
    KontenTanggalListView,
    KontenDetailView,

    KomentarUpdateView,
    KomentarDeleteView,
    ReplyKomenView,
    ReplyUpdateView,
    ReplyDeleteView,

    KategoriListView,
    KategoriDetailView,
    ContactView,
    GaleriListView,
    SaranCreateView,
    KonfigurasiUpdateView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegisterView.as_view(), name='user_register'),

    path('profil/<int:pk>' , UserProfilView.as_view() , name="user_profil"),
    path('profil/update/<int:pk>' , UserUpdateView.as_view() , name="user_update"),
    path('user/profil/<int:pk>' , UserDetailView.as_view() , name="user_detail"),
    path('update/social/<int:pk>/', UserSosmedUpdate.as_view(), name='update_social'),

    path('komunitas/', KomunitasListView.as_view(), name="komunitas_list"),

    path('' , KontenListView.as_view() , name="konten_list"),
    path('post/latest' , KontenLatestListView.as_view() , name="konten_latest"),
    path('post/tanggal/', KontenTanggalListView.as_view(), name='konten_tanggal_list'),
    path('detail/<slug:slug>' , KontenDetailView.as_view() , name="konten_detail"),

    path('reply/<int:komen_id>/', ReplyKomenView.as_view(), name='reply_komen'),
    path('update_komen/<int:komen_id>/', KomentarUpdateView.as_view(), name='komentar_update'),
    path('delete_komen/<int:komen_id>/', KomentarDeleteView.as_view(), name='komentar_delete'),

     path('reply/<int:reply_id>/edit/', ReplyUpdateView.as_view(), name='reply_update'),
     path('reply/<int:reply_id>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),

    path('kategori/' , KategoriListView.as_view() , name="kategori_list"),
    path('kategori/detail/<int:pk>' , KategoriDetailView.as_view() , name="kategori_detail"),

    path('contact/' , ContactView.as_view() , name="contact"),
    path('galeri/' , GaleriListView.as_view() , name="galeri_list"),

    path('saran/add/' , SaranCreateView.as_view() , name="saran_create"),
    path('konfigurasi/', KonfigurasiUpdateView.as_view(), name='konfigurasi'),
]
