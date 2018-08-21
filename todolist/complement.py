from datetime import datetime
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

def execute_sql(sql, *args):
	from django.db import connection
	with connection.cursor() as cursor:
		cursor.execute(sql, args)
		row = dictfetchall(cursor)
	return row

def valid_fech(value):
	from apps.user.models import User
	fec_val = datetime.strptime(str(value),"%Y-%m-%d")
	fec_may = datetime.strptime(User().my_age(),"%Y-%m-%d")
	fec_err = datetime.strptime(User().my_age(edad=False),"%Y-%m-%d")

	if fec_val > fec_may:
		raise ValidationError(_('18+'))

	if fec_val < fec_err:
		raise ValidationError(_('99+'))

class MyPaginator(Paginator):
	def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True, number_show=7, query=None, publicidad=None):
		self.number_show = number_show
		self.query = query
		self.publici = publicidad
		if publicidad:
			self.query = self.publicidad()
		super(MyPaginator, self).__init__(object_list, per_page, orphans=0,
                 allow_empty_first_page=True)
	
	def paginator_simple(self):
		self.page_init = 1
		self.page_end = self.num_pages
		if (self.ini_page() or self.previ_number()) and self.show_end():
			return range(self.page_init, self.number_show + 1)
		if self.end_number():
			return range(self.get_page_prev(), self.page_end + 1)
		if not self.previ_number():
			return range(self.obj_page.number - self.conve_numer(), self.obj_page.number + self.conve_numer() + 1)

		return self.page_range

	def publicidad(self):
		from random import randint
		query_publi = self.query
		publicida = self.publici
		new_query = []
		num_ram = randint(5,6)
		rango = range(1,len(self.query))
		num_key = 0
		num_publ = 1
		for qp in query_publi:
			if num_ram == num_publ:
				num_publ = 1
				if num_key < len(publicida):
					new_query.append(publicida[num_key])
					num_key += 1
					num_publ += 2
					num_ram = randint(5,6)
			else:
				num_publ += 1
			new_query.append(qp)
		return new_query
			
	def get_page_prev(self):
		number = self.page_end - (self.number_show - 1)
		if number < 1:
			number = 1
		return number

	def number_impar(self):
		if int(self.number_show)%2 != 0:
			return True
		else:
			return False

	def end_number(self):
		number_show = int(self.page_end - self.conve_numer())
		if self.obj_page.number > number_show:
			return True
		else:
			return False

	def conve_numer(self):
		number_show = self.number_show
		if self.number_impar():
			number_show -= 1
			number_show /= 2
		else:
			number_show /= 2
		return int(number_show)

	def previ_number(self):
		number_show = self.conve_numer()
		number_show += 1
		if self.obj_page.number < number_show:
			return True
		else:
			return False

	def show_end(self):
		if self.page_end > self.number_show:
			return True
		else:
			return False

	def ini_page(self):
		if self.obj_page.number == self.page_init:
			return True
		else:
			return False

	def get_page(self, number):
		self.obj_page = super(MyPaginator, self).get_page(number)
		return self.obj_page

def obtcod(cod, salt):
	return '{}{}{}'.format(salt, cod, salt)

def cleanhtml(text,br=False, salt='hwgksl'):
	from django.utils.html import strip_tags
	import re
	if isinstance(br,list):
		new_br = []
		for c in br:
			formato = '<{}.*?>|</{}>'.format(c['format'],c['format'])
			cleanr = re.compile(formato)
			quit_format = re.findall(cleanr, text)
			text = re.sub(cleanr, obtcod(c['format'], salt), text)
			quits_formats = {c['format']:quit_format}
			new_br.append(quits_formats)

	cleantext = strip_tags(text)
	if isinstance(br,list):
		rang2 = 0
		for c in br:
			if new_br[rang2][c['format']] != []:
				cleanr = re.compile(obtcod(c['format'], salt))
				rang = 0
				for f in new_br[rang2].values():
					cleantext = re.sub(cleanr, lambda m: devolclea(m.group(0), f, c), cleantext, count=rang)
					rang += 1
			rang2 += 1

	return str(cleantext)