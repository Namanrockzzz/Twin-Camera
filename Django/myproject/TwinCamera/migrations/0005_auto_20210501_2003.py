# Generated by Django 3.2 on 2021-05-01 14:33

import TwinCamera.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TwinCamera', '0004_alter_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='bg',
            field=models.ImageField(blank=True, null=True, upload_to=TwinCamera.models.path_and_rename),
        ),
        migrations.AlterField(
            model_name='image',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to=TwinCamera.models.path_and_rename),
        ),
        migrations.AlterField(
            model_name='image',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to=TwinCamera.models.path_and_rename),
        ),
        migrations.AlterField(
            model_name='image',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to=TwinCamera.models.path_and_rename),
        ),
        migrations.AlterField(
            model_name='image',
            name='img4',
            field=models.ImageField(blank=True, null=True, upload_to=TwinCamera.models.path_and_rename),
        ),
        migrations.AlterField(
            model_name='image',
            name='img5',
            field=models.ImageField(blank=True, null=True, upload_to=TwinCamera.models.path_and_rename),
        ),
        migrations.AlterField(
            model_name='image',
            name='img6',
            field=models.ImageField(blank=True, null=True, upload_to=TwinCamera.models.path_and_rename),
        ),
    ]
