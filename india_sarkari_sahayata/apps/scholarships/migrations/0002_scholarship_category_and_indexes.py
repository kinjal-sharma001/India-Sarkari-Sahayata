from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scholarships", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="scholarship",
            name="category",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddIndex(
            model_name="scholarship",
            index=models.Index(fields=["category"], name="scholarship_categor_610ff1_idx"),
        ),
        migrations.AddIndex(
            model_name="scholarship",
            index=models.Index(fields=["level"], name="scholarship_level_f4fd45_idx"),
        ),
    ]
