from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from panel.utils import user_directory_path

# Create your models here.

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_sender',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_receiver',
        # limit_choices_to={'is_prof': True},
    )
    content = models.TextField(blank=True, null=True, default="")
    date_sent = models.DateTimeField(auto_now_add=True)
    has_file = models.BooleanField(default=False)
    file_name = models.CharField(max_length=255, default='')
    file_extention = models.CharField(max_length=10, default='')
    is_read = models.BooleanField(default=False)
    chat_file = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'پیام {self.sender} برای {self.receiver}'