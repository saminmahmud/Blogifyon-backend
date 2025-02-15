# Generated by Django 5.1 on 2025-02-14 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_alter_review_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='profile_picture_url',
        ),
        migrations.AddField(
            model_name='author',
            name='profile_picture',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/dedwheqpz/image/upload/v1724566164/Blog_Website/Profile_Picture/eilrzwzvrrp9axkpw1u5.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
