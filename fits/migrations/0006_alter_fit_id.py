# Generated by Django 3.2.6 on 2021-08-12 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fits', '0005_alter_fit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fit',
            name='id',
            field=models.CharField(default='77c67165', editable=False, max_length=32, primary_key=True, serialize=False),
        ),
    ]