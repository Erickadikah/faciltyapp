# Generated by Django 5.0.3 on 2024-03-24 00:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0002_remove_uploadeddocument_document_name_and_more'),
        ('host', '0018_alter_client_creator_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadeddocument',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_documents', to='host.client'),
        ),
    ]