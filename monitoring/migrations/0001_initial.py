# Generated by Django 2.0.5 on 2018-05-22 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Berita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200, unique=True)),
                ('breadcrumb', models.CharField(max_length=100)),
                ('tanggal', models.DateTimeField(null=True)),
                ('penulis', models.CharField(max_length=50)),
                ('judul', models.CharField(max_length=200)),
                ('isi', models.TextField(max_length=4000)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag01', models.CharField(max_length=50)),
                ('tag02', models.CharField(max_length=50)),
                ('tag03', models.CharField(max_length=50)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='monitoring.Berita')),
            ],
        ),
    ]
