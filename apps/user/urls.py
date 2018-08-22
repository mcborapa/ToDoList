from django.urls import path
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from apps.user.views import (register, index, Login, mythings, pendingth, madeth, save_thing,
    delete_thing, chang_stat, edit_thign, edit_th, view_th)

urlpatterns = [
	path('', index, name='index'),
    path('made/', madeth, name='madeth'),
    path('edit_th/', edit_th, name='edit_th'),
    path('view_th/', view_th, name='view_th'),
    path('register/', register, name='register'),
    path('mythings/', mythings, name='mythings'),
    path('pending/', pendingth, name='pendingth'),
    path('login/', Login.as_view(), name='login'),
    path('chang_stat/', chang_stat, name='chang_stat'),
    path('edit_thign/', edit_thign, name='edit_thign'),
    path('save_thing/', save_thing, name='save_thing'),
    path('delete_thing/', delete_thing, name='delete_thing'),
    path('logout/', login_required(logout_then_login), name='logout'),
    
]