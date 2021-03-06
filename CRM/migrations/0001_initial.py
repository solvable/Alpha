# Generated by Django 2.0.1 on 2018-01-09 18:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_by', models.CharField(default=1, max_length=50)),
                ('firstName', models.CharField(max_length=20)),
                ('lastName', models.CharField(max_length=20)),
                ('fullName', models.CharField(blank=True, max_length=50)),
                ('billStreet', models.CharField(max_length=25)),
                ('billCity', models.CharField(max_length=20)),
                ('billState', models.CharField(max_length=2)),
                ('billZip', models.CharField(max_length=5)),
                ('latlng', models.CharField(blank=True, default='', max_length=100)),
                ('lat', models.FloatField(blank=True, default='', max_length=100)),
                ('lng', models.FloatField(blank=True, default='', max_length=100)),
                ('phone1', models.CharField(max_length=20)),
                ('phone2', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('source', models.CharField(choices=[('NA', 'Not Applicable'), ('AL', "Angie's List"), ('CO', 'Contractor'), ('GO', 'Google'), ('OC', 'Old Customer'), ('OT', 'Other'), ('RC', 'Recco'), ('RE', 'Realtor'), ('WS', 'Website'), ('YL', 'Yelp')], default='NA', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(default=1, on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
            },
        ),
        migrations.CreateModel(
            name='Jobsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_by', models.CharField(default=1, max_length=50)),
                ('jobStreet', models.CharField(max_length=25)),
                ('jobCity', models.CharField(max_length=20)),
                ('jobState', models.CharField(max_length=2)),
                ('jobZip', models.CharField(max_length=5)),
                ('stories', models.IntegerField()),
                ('access', models.CharField(max_length=20)),
                ('notes', models.CharField(blank=True, max_length=150)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('latlng', models.CharField(blank=True, default='', max_length=100)),
                ('lat', models.FloatField(blank=True, default=0, max_length=100)),
                ('lng', models.FloatField(blank=True, default=0, max_length=100)),
                ('customer_id', models.ForeignKey(on_delete='PROTECT', to='CRM.Customer')),
                ('user', models.ForeignKey(default=1, on_delete='PROTECT', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_type', models.CharField(blank=True, choices=[('Estimate', 'Estimate'), ('Inspection', 'Inspection'), ('Service', 'Service')], max_length=10, null=True)),
                ('problem', models.CharField(max_length=200, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('modified_by', models.CharField(default=1, max_length=50, null=True)),
                ('notes', models.TextField(default='', max_length=200, null=True)),
                ('customer_id', models.ForeignKey(on_delete='PROTECT', to='CRM.Customer')),
                ('jobsite_id', models.ForeignKey(on_delete='PROTECT', to='CRM.Jobsite')),
            ],
        ),
    ]
