# Generated by Django 4.2.1 on 2023-08-28 18:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0003_alter_proposal_prof_moshaver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='profs_arzyab',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_prof': True}, related_name='proposal_profs_arzyab', to=settings.AUTH_USER_MODEL),
        ),
    ]
