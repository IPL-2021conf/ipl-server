# Generated by Django 3.2.8 on 2021-11-03 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img_proc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImgFaceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='imgproc')),
            ],
        ),
    ]
