from django.db import models
from django.contrib.auth.models import AbstractUser
from todolist.complement import valid_fech, execute_sql
import time

class User(AbstractUser):
	email = models.EmailField('Correo Electrónico', unique=True)
	ip = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True, default=None,editable=False)
	ips = models.TextField('Ips', blank=True, null=True)
	last_ip = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True, default=None,editable=False)
	username = models.CharField('Nombre de Usuario', max_length=150,blank=True,null=True)
	birthday = models.DateField(validators=[valid_fech])
	phone = models.CharField('Número de telefono',max_length=50, blank=True, null=True)
	first_name = models.CharField('Nombres', max_length=30)
	last_name = models.CharField('Apellidos', max_length=150)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	def __str__(self):
		return self.email

	def my_age(self,edad=True):
		anhoact = int(time.strftime("%Y"))
		if edad:
			new_a = anhoact - 18
		else:
			new_a = anhoact - 99
		new_fech = time.strftime("{}-%m-%d".format(new_a))
		return new_fech

class Things(models.Model):
	id_th = models.AutoField(primary_key=True)
	name_th = models.TextField('Nombre', blank=False, null=True)#Nombre de la tarea por hacer.
	datec_th = models.DateTimeField(auto_now_add=True, editable=False) #Fecha de creacion.
	status_th = models.BooleanField(default=False) #Estatus de la tarea por hacer.
	dater_th = models.DateField(blank=False, null=True) #Fecha en qu se realizo la tarea.
	user = models.ForeignKey(User, on_delete=models.CASCADE) #Usuario que la realiza.

	def __str__(self):
		return '# {}'.format(self.id_th)

	def Paginator_Things(request, page, limit, stat_th="", us=""):
		import os
		from django.conf import settings

		sql = "SELECT * FROM user_things mt INNER JOIN user_user us ON us.id = mt.user_id WHERE us.is_active IS TRUE AND us.id = {us} {stat_th} ORDER BY mt.id_th DESC LIMIT {limit} OFFSET {offset}"
		sql2 = "SELECT COUNT(mt.id_th) FROM user_things mt INNER JOIN user_user uu ON uu.id = mt.user_id WHERE uu.is_active IS TRUE AND mt.user_id = {} {}".format(us, stat_th)
		count = execute_sql(sql2)
		things = execute_sql(sql.format(limit=limit, offset=(int(page) - 1) * (int(limit)), stat_th=stat_th, us=us))
		return {
				"things": things,
				"count": count[0]['count'],
			}
