# Generated by Django 5.0.1 on 2024-04-30 08:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_remove_generatedtest_uploaded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedtest',
            name='test_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='generatedtest',
            name='test_name',
            field=models.CharField(default='Default Test Name', max_length=255),
        ),
    ]
