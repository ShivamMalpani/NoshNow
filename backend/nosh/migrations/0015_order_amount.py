# Generated by Django 3.2.4 on 2024-01-25 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nosh', '0014_alter_paymenthistory_transactionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Amount',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]