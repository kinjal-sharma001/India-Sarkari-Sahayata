from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CandidateProfile


@receiver(post_save, sender=User)
def create_candidate_profile(sender, instance, created, **kwargs):
    if created:
        CandidateProfile.objects.create(user=instance)
