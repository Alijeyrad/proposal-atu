from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    """
        User Model For The App
        storing students and professors
    """
    
    phone_number = PhoneNumberField(blank=True, verbose_name='شماره تلفن')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    """
        Profile Model For Each User
        storing detailed information about users
    """

    ARSHAD = 'arshad'
    DOCTORA = 'doctora'

    MAGHTA_CHOICES = [
        (ARSHAD, 'ارشد'),
        (DOCTORA, 'دکتری'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    maghta = models.CharField(
        max_length=7,
        choices=MAGHTA_CHOICES,
        default=ARSHAD,
        verbose_name='مقطع',
        blank=True
    )

    student_number = models.CharField(blank=True, null=True, max_length=100, verbose_name='شماره دانشجویی')

    is_student = models.BooleanField(default=True, verbose_name='دانشجو است')
    
    is_prof = models.BooleanField(default=False, verbose_name='استاد است')

    proposal_name = models.CharField(max_length=1500)

    study_field = models.ForeignKey('StudyField', on_delete=models.CASCADE)


class StudyField(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    sub_title = models.CharField(max_length=255, verbose_name='گرایش', blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.sub_title}'



class Department(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title}'