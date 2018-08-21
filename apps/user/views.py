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
	limit = 9
	if not page:
		page = 1
	if request.user.is_authenticated:
		use = request.user.id
		pagn = Things.Paginator_Things(request, page=page, limit=limit, us=use)
		paginator = MyPaginator(range(0, pagn["count"]), limit, query=pagn["things"])
		sear = paginator.get_page(page)
		contexto = {
			'sear':sear,
			'total': pagn["count"]
		}
		return render(request, template, contexto)
	else:
		return render(request, template)

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
			_json = {'success': False, 'msj':'Ocurrio un error, vuelve a intentarlo.'}
	else:
		_json = {'success':False, 'msj':'Ocurrio un error, vuelve a intentarlo.'}
	_json = json.dumps(_json)
	return HttpResponse(_json, content_type='application/json')

@login_required
def delete_thing(request):
	js = ''
	msj = 'Ocurrio un error, vuelve a intentarlo.'
	if request.method == 'POST':
		try:
			th = int(request.POST['thing'])
			thing = Things.objects.get(pk=th)
			if thing:
				if thing.user == request.user:
					thing.delete()
					count = Things.objects.filter(user=request.user).count()
					js = {'success':True, 'count':count}
				else:
					js = {'success': False, 'msj':msj}
			else:
				js = {'success': False, 'msj':msj}
		except Exception as e:
			js = {'success': False, 'msj':msj}
	else:
		js = {'success': False, 'msj':msj}
	js = json.dumps(js)
	return HttpResponse(js, content_type='aplication/json')

@login_required
def chang_stat(request):
	js = ''
	msj = 'Ocurrio un error, vuelve a intentarlo.'
	if request.method == 'POST':
		try:
			th = int(request.POST['thing'])
			stat = request.POST['stat']
			hoy = date.today()
			if stat == 'Pendiente' or stat == 'Terminada':
				if stat == 'Pendiente':
					stat = True
					new_st = 'Terminada'
				else:
					stat = False
					new_st = 'Pendiente'
				thing = Things.objects.get(pk=th)
				if thing:
					if thing.user == request.user:
						if thing.status_th != stat:
							thing.status_th = stat
							thing.dater_th = hoy
							thing.save()

							th = thing.pk
							cont = thing.name_th
							stat = thing.status_th
							if stat:
								anho, mes, dia = str(thing.dater_th).split('-')
								fecha = '{}/{}/{}'.format(dia, mes, anho)
							else:
								anho, mes, dia = str(thing.datec_th).split('-')
								fecha = '{}/{}/{}'.format(dia[0:2], mes, anho)
							js = {'success':True, 'cont':cont, 'fecha':fecha, 'stat':stat, 'th':th}
						else:
							js = {'success': False, 'msj':msj}
					else:
						js = {'success': False, 'msj':msj}
				else:
					js = {'success': False, 'msj':msj}
			else:
				js = {'success': False, 'msj':msj}
		except Exception as e:
			js = {'success': False, 'msj':msj}
	else:
		js = {'success': False, 'msj':msj}
	js = json.dumps(js)
	return HttpResponse(js, content_type='aplication/json')

@login_required
def edit_thign(request):
	js = ''
	msj = 'Ocurrio un error, vuelve a intentarlo.'
	if request.method == 'POST':
		try:
			th = int(request.POST['thing'])
			cont = cleanhtml(request.POST['cont'], [{'format': 'br', 'replace': ''}])
			cont = cont.strip()
			check = request.POST['statch']
			if check == 'true' or check == 'false':
				if check == 'true':
					check = True
				elif check == 'false':
					check = False
				mod = False
				if cont != '':
					thing = Things.objects.get(pk=th)
					if thing:
						if thing.user == request.user:
							if thing.name_th != cont:
								thing.name_th = cont
								mod = True
							if thing.status_th != check:
								thing.status_th = check
								if check:
									hoy = date.today()
									thing.dater_th = hoy
								mod = True
							
							if mod:
								thing.save()
								cont = thing.name_th
								stat = thing.status_th
								if stat:
									anho, mes, dia = str(thing.dater_th).split('-')
									fecha = '{}/{}/{}'.format(dia, mes, anho)
								else:
									anho, mes, dia = str(thing.datec_th).split('-')
									fecha = '{}/{}/{}'.format(dia[0:2], mes, anho)
								js = {'success':True, 'cont':cont, 'fecha':fecha, 'stat':stat, 'th':th}
							else:
								js = {'success': False, 'msj':'No ha realizado ningun cambio'}
						else:
							js = {'success': False, 'msj':msj}
					else:
						js = {'success': False, 'msj':msj}
				else:
					js = {'success': False, 'msj':'No puede estar vacio. Debe ingresar un contenido'}
			else:
				js = {'success': False, 'msj':msj}
		except Exception as e:
			js = {'success': False, 'msj':msj}
	else:
		js = {'success': False, 'msj':msj}
	js = json.dumps(js)
	return HttpResponse(js, content_type='aplication/json')

@login_required
def edit_th(request):
	js = ''
	msj = 'Ocurrio un error, vuelve a intentarlo.'
	if request.method == 'POST':
		try:
			th = int(request.POST['thing'])
			thing = Things.objects.get(pk=th)
			if thing:
				if thing.user == request.user:
					th = thing.pk
					cont = thing.name_th
					stat = thing.status_th
					if stat:
						anho, mes, dia = str(thing.dater_th).split('-')
						fecha = '{}/{}/{}'.format(dia, mes, anho)
					else:
						anho, mes, dia = str(thing.datec_th).split('-')
						fecha = '{}/{}/{}'.format(dia[0:2], mes, anho)
					js = {'success':True, 'cont':cont, 'fecha':fecha, 'stat':stat, 'th':th}
				else:
					js = {'success': False, 'msj':msj}
			else:
				js = {'success': False, 'msj':msj}
		except Exception as e:
			js = {'success': False, 'msj':msj}
	else:
		js = {'success': False, 'msj':msj}
	js = json.dumps(js)
	return HttpResponse(js, content_type='aplication/json')

@login_required
def view_th(request):
	js = ''
	msj = 'Ocurrio un error, vuelve a intentarlo.'
	if request.method == 'POST':
		try:
			th = int(request.POST['thing'])
			thing = Things.objects.get(pk=th)
			if thing:
				if thing.user == request.user:
					th = thing.pk
					cont = thing.name_th
					stat = thing.status_th
					if stat:
						anho, mes, dia = str(thing.dater_th).split('-')
						fecha = '{}/{}/{}'.format(dia, mes, anho)
					else:
						anho, mes, dia = str(thing.datec_th).split('-')
						fecha = '{}/{}/{}'.format(dia[0:2], mes, anho)
					js = {'success':True, 'cont':cont, 'fecha':fecha, 'stat':stat, 'th':th}
				else:
					js = {'success': False, 'msj':msj}
			else:
				js = {'success': False, 'msj':msj}
		except Exception as e:
			js = {'success': False, 'msj':msj}
	else:
		js = {'success': False, 'msj':msj}
	js = json.dumps(js)
	return HttpResponse(js, content_type='aplication/json')

