# Generated by Django 2.1.1 on 2019-05-10 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0007_auto_20190509_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='asynctask',
            name='fixture',
            field=models.FileField(blank=True, null=True, upload_to='fixtures/'),
        ),
    ]
