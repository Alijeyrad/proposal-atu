from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

# Create your models here.

User = get_user_model()

# utility function
# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     try:
#         return 'user_{0}/{1}'.format(instance.owner.id, filename)
#     except:
#         return 'user_{0}/{1}'.format(instance.sender.id, filename)

# class Proposal(models.Model):

#     # حالت‌ها: هنوز درخواست تصویب داده نشده، در حال تصویب، تصویب شده
#     PRE_ACCEPT = 'هنوز درخواست تصویب داده نشده'
#     ACCEPTING = 'در حال تصویب'
#     ACCEPTED = 'تصویب شده'

#     STATUS_CHOICES = [
#         (PRE_ACCEPT, PRE_ACCEPT),
#         (ACCEPTING, ACCEPTING),
#         (ACCEPTED, ACCEPTED),
#     ]

#     file = models.FileField(
#         upload_to=user_directory_path,
#         validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
#     )

#     date_added = models.DateTimeField(auto_now_add=True)

#     status = models.CharField(
#         max_length=50,
#         choices=STATUS_CHOICES,
#         default=PRE_ACCEPT,
#         verbose_name='وضعیت', 
#     )

#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposal_owner')

#     # prof_rahnama = models.ForeignKey(
#     #     User,
#     #     on_delete=models.CASCADE,
#     #     related_name='proposal_profs_rahnama',
#     #     limit_choices_to={'is_prof': True},    
#     # )

#     # profs_arzyab = models.ManyToManyField(
#     #     User,
#     #     related_name='proposal_profs_arzyab',
#     #     blank=True,
#     #     limit_choices_to={'is_prof': True}, 
#     # )

#     name = models.CharField(max_length=255, default="")
#     extention = models.CharField(max_length=10, default="")

#     def __str__(self):
#         return f'{self.owner.first_name} {self.owner.last_name}'