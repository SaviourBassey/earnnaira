from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserAdditionalInformation, DailyLoginReward, ReferalReward


@receiver(post_save, sender=User)
def create_useradditionalinformation(sender, instance, created, **kwargs):
    if created:
        UserAdditionalInformation.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_useradditionalinformation(sender, instance, **kwargs):
    instance.useradditionalinformation.save()


@receiver(post_save, sender=User)
def create_dailyloginreward(sender, instance, created, **kwargs):
    if created:
        DailyLoginReward.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_dailyloginreward(sender, instance, **kwargs):
    instance.dailyloginreward.save()


@receiver(post_save, sender=User)
def create_referalreward(sender, instance, created, **kwargs):
    if created:
        ReferalReward.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_referalreward(sender, instance, **kwargs):
    instance.referalreward.save()