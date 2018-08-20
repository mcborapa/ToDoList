from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.utils import translation
from apps.user.forms import RegistroForm, Aute
from apps.user.models import User, Things
from datetime import date
from todolist.complement import MyPaginator, cleanhtml
import json
import os
import time

def index(request):
	template = 'user/index.html'
	page = request.GET.get('page')
	limit = 21
	if not page:
		page = 1
	use = request.user.id
	pagn = Things.Paginator_Things(request, page=page, limit=limit, us=use)
	paginator = MyPaginator(range(0, pagn["count"]), limit, query=pagn["things"])
	sear = paginator.get_page(page)
	contexto = {
		'sear':sear,
		'total': pagn["count"]
	}
	return render(request, template, contexto)

def register(request):
	form = RegistroForm()
	template = 'public/register.html'
	get_success_url = reverse_lazy('user:index')
	if request.user.is_authenticated:
		return HttpResponseRedirect(get_success_url)
	else:
		if request.method == 'POST':
			form = RegistroForm(request.POST)
			if form.is_valid():
				user = form.save(commit=False)
				user.ip_create = request.META.get('REMOTE_ADDR')
				user.ip_last = request.META.get('REMOTE_ADDR')
				user.ips = request.META.get('REMOTE_ADDR')
				user.save()
				auth_login(request, user)
				return HttpResponseRedirect(get_success_url)

	context = {'form': form}
	return render(request, template, context)

class Login(LoginView):
	template_name = 'public/login.html'
	form_class = Aute
	get_success_url = reverse_lazy('user:index')

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url)
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		ipnew = self.request.META.get('REMOTE_ADDR')
		user = form.get_user()
		user.ip_last = ipnew
		if ipnew not in user.ips:
			user.ips += ',{}'.format(ipnew)
		user.save()
		auth_login(self.request, user)
		return HttpResponseRedirect(self.get_success_url)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		current_site = get_current_site(self.request)
		context.update({
			self.redirect_field_name: self.get_redirect_url(),
			'site': current_site,
			'site_name': current_site.name,
		})
		if 'form' not in context:
			if self.request.method == 'POST':
				context['form'] = self.form_class(self.request.POST)
			else:
				context['form'] = self.form_class
		return context

	def post(self, request, *args, **kwargs):
		var = request.POST
		form = self.form_class(var)
		if True:
			return super().post(request, *args, **kwargs)
		return self.render_to_response(self.get_context_data(form=form))

@login_required
def mythings(request):
	template = 'user/mythings.html'
	page = request.GET.get('page')
	limit = 20
	if not page:
		page = 1
	use = request.user.id
	pagn = Things.Paginator_Things(request, page=page, limit=limit, us=use)
	paginator = MyPaginator(range(0, pagn["count"]), limit, query=pagn["things"])
	sear = paginator.get_page(page)
	contexto = {
		'sear':sear,
		'total': pagn["count"]
	}
	return render(request, template, contexto)

@login_required
def pendingth(request):
	template = 'user/pending.html'
	page = request.GET.get('page')
	limit = 20
	if not page:
		page = 1
	use = request.user.id
	status = "AND mt.status_th IS FALSE"
	pagn = Things.Paginator_Things(request, page=page, limit=limit, us=use, stat_th=status)
	paginator = MyPaginator(range(0, pagn["count"]), limit, query=pagn["things"])
	sear = paginator.get_page(page)
	contexto = {
		'sear':sear,
		'total': pagn["count"]
	}
	return render(request, template, contexto)

@login_required
def madeth(request):
	template = 'user/made.html'
	page = request.GET.get('page')
	limit = 20
	if not page:
		page = 1
	use = request.user.id
	status = "AND mt.status_th IS TRUE"
	pagn = Things.Paginator_Things(request, page=page, limit=limit, us=use, stat_th=status)
	paginator = MyPaginator(range(0, pagn["count"]), limit, query=pagn["things"])
	sear = paginator.get_page(page)
	contexto = {
		'sear':sear,
		'total': pagn["count"]
	}
	return render(request, template, contexto)

@login_required
def save_thing(request):
	_json = ''
	template = 'user/create.html'
	if request.method == 'POST':
		try:
			limit = 1
			text = cleanhtml(request.POST['cont'], [{'format': 'br', 'replace': ''}])
			cont = text.strip()
			if cont != '':
				thi = Things()
				thi.name_th = cont
				thi.user = request.user
				thi.save()
				pagn = Things.Paginator_Things(request, page=limit, limit=limit, us=request.user.id)
				contexto = {'pag':pagn['things'][0]}
				return render(request,template, contexto)
			else:
				_json = {'success': False, 'msj':'No puede estar vacio. Debe ingresar un contenido'}
		except Exception as e:
			print('ERror:', e)
			_json = {'success': False, 'msj':'Ocurrio un error, vuelve a intentarlo.'}
	else:
		_json = {'success':False, 'msj':'Ocurrio un error, vuelve a intentarlo.'}
	_json = json.dumps(_json)
	return HttpResponse(_json, content_type='application/json')

