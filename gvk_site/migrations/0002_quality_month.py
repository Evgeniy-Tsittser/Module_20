# Generated by Django 5.1.3 on 2024-11-17 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gvk_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quality',
            name='month',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
