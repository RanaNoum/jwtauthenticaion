# Generated by Django 5.0.4 on 2024-05-09 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricingestimate',
            name='additional_features',
            field=models.CharField(blank=True, choices=[('messaging', 'Messaging'), ('geolocation', 'Geolocation'), ('shopping_cart', 'Shopping Cart & Orders History'), ('cms', 'Basic CMS for Content Uploading'), ('bluetooth', 'Bluetooth Connectivity'), ('camera', 'Camera (QR Code Scanning)'), ('multi_language', 'Multi-language Support'), ('social_media', 'Social Media Sharing')], default='Messages', max_length=100),
        ),
    ]
