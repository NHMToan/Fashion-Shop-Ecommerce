# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20190419_0459'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('pants', 'Pants'), ('top', 'Top'), ('accessory', 'Accessory'), ('hat', 'Hat'), ('footerwear', 'Footerwear')], default='accessory', max_length=120),
        ),
    ]
