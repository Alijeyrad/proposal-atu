# Generated by Django 4.2.1 on 2023-08-29 13:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import panel.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='', null=True)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('has_file', models.BooleanField(default=False)),
                ('file_name', models.CharField(default='', max_length=255)),
                ('file_extention', models.CharField(default='', max_length=10)),
                ('is_read', models.BooleanField(default=False)),
                ('chat_file', models.FileField(blank=True, null=True, upload_to=panel.utils.user_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
