# Generated by Django 3.2 on 2021-05-01 14:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('TwinCamera', '0003_remove_image_sid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]