# Generated by Django 5.1.5 on 2025-01-26 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0004_address'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DietCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='diet_categories/')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Bkash', 'Bkash'), ('Nagad', 'Nagad')], max_length=50)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('coupon_voucher', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_summary', models.TextField()),
                ('billing_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='medicine.address')),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_address', to='medicine.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=50)),
                ('meal', models.TextField()),
                ('quantity', models.CharField(max_length=100)),
                ('diet_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicine.dietcategory')),
            ],
        ),
    ]
