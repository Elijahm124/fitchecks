# Generated by Django 3.2.6 on 2021-08-12 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fits', '0004_auto_20210811_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fit',
            name='id',
            field=models.CharField(default='6d1afcaf', editable=False, max_length=32, primary_key=True, serialize=False),
        ),
    ]
