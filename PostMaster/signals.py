from django.db.models.signals import post_save
from django.dispatch import receiver
from PostMaster.models import Package, Tracking, Subscriber
import requests


@receiver(post_save, sender=Package)
def on_package_save(sender, instance: Package, **kwargs):
    """
    Creates an associated Tracking object when a new Package is created.

    :param sender: model that triggered the action
    :type sender: Package
    :param instance: Instance of the model that triggered the action
    :type instance: Package
    """

    if not instance.has_tracking:
        tracking = Tracking(package=instance)
        tracking.save()
        instance.has_tracking = True
        print("Making a new package")
        instance.save()


@receiver(post_save, sender=Subscriber)
def on_subscriber_save(sender, instance: Subscriber, **kwargs):
    """
    Maps the subscriber's Minecraft username to their UUID

    :param sender: model that triggered the action
    :type sender: Subscriber
    :param instance: Instance of the model that triggered the action
    :type instance: Subscriber
    """

    post_save.disconnect(on_subscriber_save, sender=Subscriber)

    # Send welcome email if new subscriber
    if not instance.welcome_email_sent:
        instance.welcome_email()
        instance.welcome_email_sent = True

    # Update subscriber UUID
    res = requests.get(f"https://api.eternal.gs/user/{instance.username}")
    if res.ok:
        user_uuid = str(res.json().get('uuid'))
    else:
        user_uuid = "not_found"

    # Set UUID to the UUID of the mapped username
    instance.uuid = user_uuid
    instance.save()

    post_save.connect(on_subscriber_save, sender=Subscriber)


@receiver(post_save, sender=Tracking)
def on_tracking_update(sender, instance: Tracking, **kwargs):
    """
    Sends update emails to all people subscribed to the tracking ID.

    :param sender: model that triggered the action
    :type sender: Tracking
    :param instance: Instance of the model that triggered the action
    :type instance: Tracking
    """

    subscribers = Subscriber.objects.filter(subscriptions__tracking_code=instance.tracking_code)

    for subscriber in subscribers:
        subscriber.tracking_update_email(instance.tracking_code)
