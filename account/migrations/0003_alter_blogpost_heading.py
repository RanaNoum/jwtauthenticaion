# Generated by Django 4.0.3 on 2024-04-28 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_blogpost_heading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='heading',
            field=models.CharField(max_length=255),
        ),
    ]