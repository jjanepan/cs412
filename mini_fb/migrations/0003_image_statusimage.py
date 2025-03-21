# Generated by Django 5.1.6 on 2025-03-05 22:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0002_statusmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='images/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.profile')),
            ],
        ),
        migrations.CreateModel(
            name='StatusImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.image')),
                ('status_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.statusmessage')),
            ],
        ),
    ]
