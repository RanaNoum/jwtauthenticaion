# Generated by Django 4.0.3 on 2024-03-28 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_project_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='comments',
            field=models.ManyToManyField(to='account.comment'),
        ),
    ]
