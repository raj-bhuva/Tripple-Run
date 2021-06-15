from django.urls import path
from . import views

# for urlpatterns + urlpatterns import this below two line
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    # path('index', views.home, name='home'),
    path("products/", views.products, name="products"),
    path("products/<slug>/", views.newdef, name='products'),
    path('singal-products/<id>/', views.singal_product, name='singal-products'),
    path("register", views.register, name="register"),

    path('login', views.login, name="login"),
    path("logout", views.logout, name="logout"),

    path('search/', views.search, name='search'),
    path('search/<query>/', views.search1, name='search'),
    path('activate/<uidb64>/<token>',
         views.activate, name='activate'),
    path('setnewpassword/<uidb64>/<token>',
         views.setnewpassword, name='setnewpassword'),
    path('forgot', views.forgot, name="forgot"),
    # path('list/', views.product_list),
    # path('search_auto', views.search_auto, name='search_auto'),
    # for wishlist
    # path('like/<int:pk>', views.wishlist, name='like_post'),
    # path('dislike/<int:pk>', views.removewishlist, name='removewishlist'),
    # path('wishlist', views.getwishlist, name="wishlist"),
    
    # path('wishlist?<str:name>=<int:pk>', views.ggetwishlist, name="gwishlist"),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
