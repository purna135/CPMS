# Generated by Django 2.1.5 on 2019-01-28 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='id',
        ),
        migrations.AlterField(
            model_name='project',
            name='project_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
