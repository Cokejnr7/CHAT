# Generated by Django 4.1.7 on 2023-08-16 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_userprofile_bio_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female')], default='m', max_length=20),
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='authentication.userprofile')),
            ],
        ),
    ]
