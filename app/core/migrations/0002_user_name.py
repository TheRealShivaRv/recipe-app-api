# Generated by Django 2.1.15 on 2021-12-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='N/A', max_length=255),
            preserve_default=False,
        ),
    ]