# Generated by Django 5.1.7 on 2025-04-01 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_post_upvotes_alter_post_upvoters_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
