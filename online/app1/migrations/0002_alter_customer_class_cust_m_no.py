# Generated by Django 3.2.5 on 2021-08-11 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_class',
            name='cust_m_no',
            field=models.PositiveIntegerField(default=0, max_length=10, verbose_name='Mobile no'),
        ),
    ]
