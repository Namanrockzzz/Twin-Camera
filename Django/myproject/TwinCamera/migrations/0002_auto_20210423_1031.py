# Generated by Django 3.2 on 2021-04-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TwinCamera', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='bg',
            field=models.ImageField(default='download.png', upload_to='images'),
        ),
        migrations.AddField(
            model_name='image',
            name='img1',
            field=models.ImageField(default='download.png', upload_to='images'),
        ),
        migrations.AddField(
            model_name='image',
            name='img2',
            field=models.ImageField(default='download.png', upload_to='images'),
        ),
        migrations.AddField(
            model_name='image',
            name='img3',
            field=models.ImageField(default='download.png', upload_to='images'),
        ),
        migrations.AddField(
            model_name='image',
            name='img4',
            field=models.ImageField(default='download.png', upload_to='images'),
        ),
        migrations.AddField(
            model_name='image',
            name='img5',
            field=models.ImageField(default='download.png', upload_to='images'),
        ),
        migrations.AddField(
            model_name='image',
            name='img6',
            field=models.ImageField(default='download.png', upload_to='images'),
        ),
    ]
