# Generated by Django 3.2.13 on 2022-05-22 09:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(20)], verbose_name='제목')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('location', models.CharField(max_length=50, verbose_name='주소')),
                ('gather_count', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='모집인원')),
                ('category', models.CharField(max_length=10, verbose_name='모집분야')),
                ('favor', models.CharField(max_length=50, verbose_name='우대사항')),
                ('content', models.TextField(verbose_name='내용')),
                ('pay', models.CharField(max_length=50, verbose_name='급여액')),
                ('work_time', models.CharField(max_length=50, verbose_name='근무시간')),
                ('call_number', models.CharField(max_length=13, verbose_name='연락처')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
