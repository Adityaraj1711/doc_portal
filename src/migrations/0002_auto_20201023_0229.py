# Generated by Django 3.1.2 on 2020-10-22 20:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procedure', models.CharField(default='', max_length=30, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='generalentry',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.CreateModel(
            name='ProcedureForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(blank=True, default='', max_length=100)),
                ('age', models.IntegerField(default='', max_length=2)),
                ('mobile_number', models.CharField(default='', max_length=10)),
                ('area_of_treatment', models.TextField(blank=True, default='', max_length=3000)),
                ('cost', models.CharField(blank=True, default='', max_length=2000)),
                ('result', models.TextField(blank=True, default='', max_length=4000)),
                ('remark', models.TextField(blank=True, default='', max_length=4000)),
                ('no_of_session', models.IntegerField(default=0)),
                ('settings_dose', models.TextField(default='', max_length=20000)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('procedure', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='src.procedure')),
            ],
        ),
    ]