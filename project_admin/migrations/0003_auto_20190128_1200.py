# Generated by Django 2.1.5 on 2019-01-28 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_admin', '0002_auto_20190128_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='project_id',
            field=models.CharField(max_length=50),
        ),
    ]
