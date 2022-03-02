from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile, ProfileStatus


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print("CREATED", created)
    if created:
        Profile.objects.create(user=instance)

        # profile = Profile.objects.create(user=instance)
        # ProfileStatus.objects.create(user_profile=profile)
