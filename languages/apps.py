from django.apps import AppConfig


class LanguagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'languages'


class YourAppConfig(AppConfig): # Replace 'yourapp' with the actual name of your app
    name = 'yourapp'

    def ready(self):  # This method is called when the app is ready
        from django.contrib.auth import get_user_model  # Import the User model
        from django.db.models.signals import post_save  # Import post_save signal
        from .models import Profile  # Import your Profile model
        User = get_user_model()  # Get the User model dynamically
        
        # Define a function to create a Profile when a User is created
        def create_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)
        # Connect the create_profile function to the post_save signal of the User model
        post_save.connect(create_profile, sender=User)