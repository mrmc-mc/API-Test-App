# Generated by Django 4.0.4 on 2022-04-30 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_oauthinfo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='image_file',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='national_code',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='can_trade',
            field=models.BooleanField(default=True, verbose_name='User Status'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.CreateModel(
            name='UserMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Time')),
                ('image_file', models.FileField(upload_to=users.utils.user_upload_dir, verbose_name='Profile Image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]