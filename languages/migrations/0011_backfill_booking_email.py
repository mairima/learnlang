# languages/migrations/0011_backfill_booking_email.py
from django.db import migrations


def fill_missing_booking_emails(apps, schema_editor):
    Booking = apps.get_model("languages", "Booking")

    # Fill NULL emails from related user.email; otherwise use a stable placeholder
    qs = Booking.objects.filter(email__isnull=True)
    for b in qs.iterator():
        user_email = ""
        # Guard for historical relations
        if getattr(b, "user_id", None) and getattr(b, "user", None):
            user_email = getattr(b.user, "email", "") or ""
        b.email = user_email or f"no-email-booking-{b.pk}@placeholder.local"
        b.save(update_fields=["email"])


class Migration(migrations.Migration):

    # IMPORTANT: set this to the migration *immediately BEFORE* the "0010_alter_booking_email_*" migration.
    # Example: if your folder shows ".../0009_something.py" then "0010_alter_booking_email_...py",
    # put ("languages", "0009_something") here (WITHOUT ".py").
    dependencies = [
        ("languages", "0009_remove_booking_date_remove_booking_time_and_more"),
    ]

    operations = [
        migrations.RunPython(fill_missing_booking_emails, reverse_code=migrations.RunPython.noop),
    ]
