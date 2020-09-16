# Generated by Django 3.1 on 2020-09-16 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_uploadpdf_pdf_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadpdf',
            name='zip_file',
            field=models.FileField(blank=True, upload_to='zip_file'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'USER'), ('admin', 'ADMIN')], default='user', max_length=5, null=True),
        ),
    ]