# Generated by Django 3.2.7 on 2021-10-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_contact_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=5000)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('address1', models.CharField(default='', max_length=100)),
                ('address2', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=50)),
                ('zip_code', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
