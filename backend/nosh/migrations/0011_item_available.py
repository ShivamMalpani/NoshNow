# Generated by Django 3.2.4 on 2024-01-23 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nosh', '0010_auto_20240123_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
