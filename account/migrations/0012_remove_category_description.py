# Generated by Django 4.0.3 on 2024-03-28 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_blogpost_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
    ]
