# Generated by Django 4.2.4 on 2023-09-02 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/products', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность поста')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время подачи')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ('-is_active', 'title'),
            },
        ),
        migrations.CreateModel(
            name='PostRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_app.post')),
            ],
            options={
                'verbose_name': 'Рейтинг к новости',
                'verbose_name_plural': 'Рейтинги к новостям',
                'ordering': ('-post', 'author'),
            },
        ),
        migrations.CreateModel(
            name='PostComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='', verbose_name='Текст комментария')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время создания')),
                ('author', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='blog_app.post', verbose_name='К какому посту')),
            ],
            options={
                'verbose_name': 'Комментарий к посту',
                'verbose_name_plural': 'Комментарии к постам',
                'ordering': ('-date_time', 'post'),
            },
        ),
    ]