# Generated by Django 5.1 on 2025-02-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_remove_author_profile_picture_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_profile_picture/default_pic.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
