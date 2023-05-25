from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Role


@receiver(post_save, sender=User)
def profile_update(sender, instance, created, **kwargs):
    print('Profile signal')
    if created:
        user = instance
        role = Role.objects.get(id=1)
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role = role
        )


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    # print('update_user', **kwargs)
    profile = instance
    user = profile.user
    user.first_name = profile.first_name
    user.username = profile.username
    user.email = profile.email
    user.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print('Deleting user...')
