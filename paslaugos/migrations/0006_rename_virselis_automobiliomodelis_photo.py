# Generated by Django 4.1.7 on 2023-03-13 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("paslaugos", "0005_automobiliomodelis_virselis"),
    ]

    operations = [
        migrations.RenameField(
            model_name="automobiliomodelis",
            old_name="virselis",
            new_name="photo",
        ),
    ]
