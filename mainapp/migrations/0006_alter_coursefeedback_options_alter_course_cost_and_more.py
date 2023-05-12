# Generated by Django 4.1.2 on 2023-05-12 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0005_coursefeedback_created_coursefeedback_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursefeedback',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='course',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Cost'),
        ),
        migrations.AlterField(
            model_name='course',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='coursefeedback',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.course', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='coursefeedback',
            name='feedback',
            field=models.TextField(default='Без отзыва', verbose_name='Feedback'),
        ),
        migrations.AlterField(
            model_name='coursefeedback',
            name='rating',
            field=models.SmallIntegerField(choices=[(5, '⭐⭐⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (3, '⭐⭐⭐'), (2, '⭐⭐'), (1, '⭐')], default=5, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='coursefeedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='courseteacher',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='courseteacher',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.course', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='num',
            field=models.PositiveIntegerField(default=0, verbose_name='Lesson number'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='news',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='news',
            name='body_as_markdown',
            field=models.BooleanField(default=False, verbose_name='Markdown markup'),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='news',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AlterField(
            model_name='news',
            name='preamble',
            field=models.CharField(max_length=1024, verbose_name='Preamble'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Article title'),
        ),
        migrations.AlterField(
            model_name='news',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
    ]