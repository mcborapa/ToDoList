# Generated by Django 2.1 on 2018-08-19 22:22

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import todolist.complement


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('ip', models.GenericIPAddressField(blank=True, default=None, editable=False, null=True, protocol='IPv4')),
                ('ips', models.TextField(blank=True, null=True, verbose_name='Ips')),
                ('last_ip', models.GenericIPAddressField(blank=True, default=None, editable=False, null=True, protocol='IPv4')),
                ('username', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre de Usuario')),
                ('birthday', models.DateField(validators=[todolist.complement.valid_fech])),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Número de telefono')),
                ('first_name', models.CharField(max_length=30, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Things',
            fields=[
                ('id_th', models.AutoField(primary_key=True, serialize=False)),
                ('name_th', models.CharField(max_length=255, verbose_name='Nombre')),
                ('datec_th', models.DateTimeField(auto_now_add=True)),
                ('status_th', models.BooleanField(default=False)),
                ('dater_th', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
