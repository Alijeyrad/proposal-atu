from django.db import models
from django.core.validators import FileExtensionValidator
from .utils import user_directory_path
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels

# Create your models here.

User = get_user_model()

class Proposal(models.Model):
    """
        model to keep proposal information
    """

    objects = jmodels.jManager()

    BAR_RAHNAMA1 = 'بررسی توسط استاد راهنما'
    TA_ARZYAB2 = 'در انتظار تعیین ارزیاب'
    ARZYABI3 = 'در حال ارزیابی'
    REJECTED4 = 'رد شده'
    ACCEPTED5 = 'تصویب شده'

    STATUS_CHOICES = [
        (BAR_RAHNAMA1, BAR_RAHNAMA1),
        (TA_ARZYAB2, TA_ARZYAB2),
        (ARZYABI3, ARZYABI3),
        (REJECTED4, REJECTED4),
        (ACCEPTED5, ACCEPTED5),
    ]

    file = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
    )
    date_added = jmodels.jDateField(auto_now_add=True)
    date_edited = jmodels.jDateField(auto_now=True)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=BAR_RAHNAMA1,
        verbose_name='وضعیت', 
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposal_owner')

    prof_rahnama = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proposal_profs_rahnama',
        # limit_choices_to={'is_prof': True},
        blank=True,
        null=True,
    )
    
    prof_moshaver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proposal_profs_moshaver',
        # limit_choices_to={'is_prof': True},
        blank=True,
        null=True,
    )

    profs_arzyab = models.ManyToManyField(
        User,
        related_name='proposal_profs_arzyab',
        blank=True,
        # limit_choices_to={'is_prof': True},
    )

    name = models.CharField(max_length=1500, default="")
    extention = models.CharField(max_length=10, default="")

    def __str__(self):
        return f'{self.owner.first_name} {self.owner.last_name}'
