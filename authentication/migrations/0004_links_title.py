# Generated by Django 4.1.7 on 2023-08-16 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_gender_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='title',
            field=models.CharField(default='social_link', max_length=30),
        ),
    ]