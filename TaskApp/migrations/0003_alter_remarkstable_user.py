# Generated by Django 5.0.3 on 2024-03-31 08:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskApp', '0002_rename_updated_at_tasktable_completed_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='remarkstable',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remark_set', to=settings.AUTH_USER_MODEL),
        ),
    ]