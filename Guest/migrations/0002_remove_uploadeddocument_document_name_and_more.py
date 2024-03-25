# Generated by Django 5.0.3 on 2024-03-23 23:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0001_initial'),
        ('host', '0017_remove_message_recipient_message_recipient_client_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadeddocument',
            name='document_name',
        ),
        migrations.RemoveField(
            model_name='uploadeddocument',
            name='document_type',
        ),
        migrations.RemoveField(
            model_name='uploadeddocument',
            name='upload_file',
        ),
        migrations.RemoveField(
            model_name='uploadeddocument',
            name='user',
        ),
        migrations.AddField(
            model_name='uploadeddocument',
            name='description',
            field=models.CharField(default='No description provided', max_length=255),
        ),
        migrations.AddField(
            model_name='uploadeddocument',
            name='file',
            field=models.FileField(default='default/file.pdf', upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='uploadeddocument',
            name='recipient_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_documents', to='host.client'),
        ),
        migrations.AddField(
            model_name='uploadeddocument',
            name='recipient_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='uploadeddocument',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]