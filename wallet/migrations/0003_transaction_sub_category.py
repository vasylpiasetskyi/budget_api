# Generated by Django 4.1 on 2022-10-19 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_alter_currency_exchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_sub_category', to='wallet.subcategory'),
        ),
    ]
