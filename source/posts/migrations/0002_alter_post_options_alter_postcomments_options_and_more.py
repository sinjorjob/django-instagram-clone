# Generated by Django 4.0.5 on 2022-06-12 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': '投稿データ', 'verbose_name_plural': '投稿データ'},
        ),
        migrations.AlterModelOptions(
            name='postcomments',
            options={'verbose_name': 'コメント', 'verbose_name_plural': 'コメント'},
        ),
        migrations.AlterModelOptions(
            name='postlikes',
            options={'verbose_name': 'いいね', 'verbose_name_plural': 'いいね'},
        ),
    ]