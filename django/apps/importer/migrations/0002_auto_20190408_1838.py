# Generated by Django 2.1.1 on 2019-04-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='importattempt',
            name='s3_bucket',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='importattempt',
            name='import_method',
            field=models.CharField(blank=True, choices=[('iRODS', 'iRODS'), ('CyVerse', 'CyVerse'), ('S3', 'S3'), ('File', 'File')], default='File', max_length=1),
        ),
    ]
