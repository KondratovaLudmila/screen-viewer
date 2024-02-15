# Generated by Django 5.0.1 on 2024-02-12 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0003_remove_screenshot_name_alter_screenshot_path'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='screenshot',
            name='folder_idx',
        ),
        migrations.RemoveField(
            model_name='screenshot',
            name='folder',
        ),
        migrations.AddField(
            model_name='screenshot',
            name='screen_date',
            field=models.DateField(null=True),
        ),
        migrations.AddIndex(
            model_name='screenshot',
            index=models.Index(fields=['screen_date'], name='screen_date_idx'),
        ),
    ]
