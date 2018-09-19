# Generated by Django 2.1.1 on 2018-09-13 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('size', models.BigIntegerField()),
                ('path', models.CharField(max_length=512)),
                ('extension', models.CharField(max_length=10)),
                ('date_created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('size', models.BigIntegerField()),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_manager.Folder')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_manager.Folder'),
        ),
    ]
