# Generated by Django 4.1.7 on 2023-08-16 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_links_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Links',
            new_name='Link',
        ),
        migrations.AlterModelOptions(
            name='link',
            options={'verbose_name': 'links'},
        ),
    ]
