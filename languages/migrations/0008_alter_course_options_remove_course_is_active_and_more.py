from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("languages", "0007_rename_course_name_to_title"),
    ]

    operations = [
        # Keep your Meta options change
        migrations.AlterModelOptions(
            name="course",
            options={"ordering": ("start_date", "title")},
        ),

        # Remove old fields if they existed
        migrations.RemoveField(
            model_name="course",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="course",
            name="weekend_only",
        ),

        # Add Booking.status with a proper default
        migrations.AddField(
            model_name="booking",
            name="status",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("PENDING", "Pending"),
                    ("CONFIRMED", "Confirmed"),
                    ("CANCELLED", "Cancelled"),
                ],
                default="PENDING",
            ),
        ),

        # Keep other field alterations
        migrations.AlterField(
            model_name="course",
            name="capacity",
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name="course",
            name="title",
            field=models.CharField(max_length=200),
        ),

        # ---------- IMPORTANT: Backfill date columns BEFORE making them non-null ----------
        # If start_date is NULL, set a sensible placeholder date
        migrations.RunSQL(
            "UPDATE languages_course SET start_date = '2025-11-03' WHERE start_date IS NULL;"
        ),
        # If end_date is NULL, copy start_date (which is guaranteed non-null after the update above)
        # If both were NULL, start_date was just set to '2025-11-03', so end_date becomes the same.
        migrations.RunSQL(
            "UPDATE languages_course SET end_date = COALESCE(end_date, start_date);"
        ),

        # Now make the fields non-nullable with NO bogus defaults
        migrations.AlterField(
            model_name="course",
            name="start_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="course",
            name="end_date",
            field=models.DateField(),
        ),
        # -------------------------------------------------------------------------------
    ]