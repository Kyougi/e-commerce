from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<str:title>", views.listing, name="listing"),
    path('comments/<str:title>', views.comments, name='comments'),
    path('addWatchlist/<int:id>/', views.addWatchlist, name='addWatchlist'),
    path('removeWatchlist/<int:id>/', views.removeWatchlist, name='removeWatchlist'),
    path('category/<str:category>', views.category, name='category'),
    path('watchlist/', views.watchlist, name='watchlist')
] 


