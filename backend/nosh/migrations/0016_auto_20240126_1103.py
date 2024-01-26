# Generated by Django 3.2.4 on 2024-01-26 11:03

from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import nosh.enum


class Migration(migrations.Migration):

    dependencies = [
        ('nosh', '0015_order_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='TransactionID',
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='OrderID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='nosh.order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='Reason',
            field=enumfields.fields.EnumField(default='order_cancellation', enum=nosh.enum.PaymentReason, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='TransactionID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
