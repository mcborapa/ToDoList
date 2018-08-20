from django.urls import path
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from apps.user.views import register, index, Login, mythings, pendingth, madeth, save_thing

urlpatterns = [
	path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(logout_then_login), name='logout'),
    path('mythings/', mythings, name='mythings'),
    path('pending/', pendingth, name='pendingth'),
    path('made/', madeth, name='madeth'),
    path('save_thing/', save_thing, name='save_thing'),
]