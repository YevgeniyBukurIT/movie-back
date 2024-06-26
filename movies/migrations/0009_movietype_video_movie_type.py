# Generated by Django 4.1.7 on 2023-05-17 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_technicalsupportuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('movie', 'Movie'), ('series', 'Series')], max_length=10)),
            ],
            options={
                'verbose_name': 'Movie Type',
                'verbose_name_plural': 'Movie Types',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('video_file', models.FileField(upload_to='videos/')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie', verbose_name='Movie')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.movietype', verbose_name='MovieType'),
        ),
    ]
