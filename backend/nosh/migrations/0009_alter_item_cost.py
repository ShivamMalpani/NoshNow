# Generated by Django 4.2.3 on 2024-01-21 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nosh', '0008_item_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]