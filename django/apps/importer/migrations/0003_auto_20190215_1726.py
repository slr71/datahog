# Generated by Django 2.1.1 on 2019-02-15 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0002_auto_20190204_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importattempt',
            name='in_progress',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='importattempt',
            name='irods_host',
            field=models.CharField(blank=True, default='data.cyverse.org', max_length=64),
        ),
        migrations.AlterField(
            model_name='importattempt',
            name='irods_port',
            field=models.CharField(blank=True, default='1247', max_length=64),
        ),
        migrations.AlterField(
            model_name='importattempt',
            name='irods_zone',
            field=models.CharField(blank=True, default='iplant', max_length=64),
        ),
    ]
