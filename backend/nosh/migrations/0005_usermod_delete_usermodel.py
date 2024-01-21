# Generated by Django 4.2.3 on 2024-01-20 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nosh', '0004_rename_user_usermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMod',
            fields=[
                ('UserID', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('mobile_no', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('profile_pic', models.URLField()),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='UserModel',
        ),
    ]