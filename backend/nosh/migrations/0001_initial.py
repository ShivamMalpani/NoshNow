# Generated by Django 4.2.3 on 2024-02-11 12:31

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("student", "Student"),
                            ("restaurant", "Restaurant"),
                            ("driver", "Driver"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("mobile_no", models.CharField(blank=True, max_length=10, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("profile_pic", models.URLField(blank=True, null=True)),
                ("amount", models.IntegerField(default=0)),
                ("email_verified", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("OrderID", models.AutoField(primary_key=True, serialize=False)),
                ("CustomerID", models.IntegerField()),
                ("Address", models.CharField(max_length=255)),
                ("Status", models.CharField(max_length=50)),
                ("Amount", models.IntegerField()),
                ("PaymentStatus", models.CharField(max_length=50)),
                ("PaymentType", models.CharField(max_length=100)),
                ("DeliveredBy", models.IntegerField(blank=True, null=True)),
                ("CreatedAt", models.DateTimeField(auto_now_add=True)),
                ("DeliveredAt", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("image", models.URLField(default=None, null=True)),
                ("address", models.CharField(max_length=255)),
                ("owner_id", models.IntegerField()),
                ("value", models.IntegerField(default=0)),
                ("rating", models.FloatField(null=True)),
                ("created_at", models.TimeField(auto_now_add=True)),
                ("start_time", models.TimeField(default="00:00")),
                ("end_time", models.TimeField(default="23:59")),
            ],
        ),
        migrations.CreateModel(
            name="UserMod",
            fields=[
                ("UserID", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.TextField()),
                ("last_name", models.TextField()),
                ("mobile_no", models.TextField()),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("profile_pic", models.URLField()),
                ("amount", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="PaymentHistory",
            fields=[
                ("TransactionID", models.AutoField(primary_key=True, serialize=False)),
                ("UserID", models.IntegerField()),
                ("Payee", models.IntegerField()),
                ("Amount", models.IntegerField()),
                ("Timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "Reason",
                    models.CharField(
                        choices=[
                            ("order_cancellation", "Order Cancellation"),
                            ("order_place", "Order Place"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "OrderID",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nosh.order",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OTP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("OTP", models.CharField(max_length=64)),
                ("expiration_time", models.DateTimeField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="RestaurantID",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nosh.restaurant"
            ),
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("cost", models.IntegerField(default=0)),
                ("description", models.TextField()),
                ("instant_item", models.BooleanField(default=False)),
                ("available", models.BooleanField(default=True)),
                ("quantity", models.IntegerField(default=0)),
                ("image", models.URLField(default=None, null=True)),
                ("rating", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "restaurant_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nosh.restaurant",
                    ),
                ),
            ],
        ),
    ]
