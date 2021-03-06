# Generated by Django 2.1.7 on 2019-03-12 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poligon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=20)),
                ('status', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Tacka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_koordinata', models.FloatField()),
                ('y_koordinata', models.FloatField()),
                ('redni_br', models.IntegerField(default=-1)),
                ('poligon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poligon.Poligon')),
            ],
        ),
    ]
