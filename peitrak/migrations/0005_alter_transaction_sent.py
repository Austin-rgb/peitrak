# Generated by Django 4.2.14 on 2024-07-13 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peitrak', '0004_transaction_remove_completedtransaction_destination_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='sent',
            field=models.BooleanField(default=True),
        ),
    ]
