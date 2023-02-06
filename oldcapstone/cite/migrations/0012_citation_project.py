# Generated by Django 4.1 on 2023-01-23 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cite', '0011_remove_project_articles_citation_project_citations'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='cite.project'),
        ),
    ]