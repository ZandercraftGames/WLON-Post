import uuid

from django.db import models
from django.core.mail import send_mail
from multi_form_view import MultiFormView


class Nation(models.Model):
    class Meta:
        verbose_name = "Nation"
        verbose_name_plural = "Nations"

    def __str__(self):
        return self.name

    # Nation Properties
    code = models.CharField("Unique Code for Nation", primary_key=True, max_length=4)
    name = models.CharField("Nation's Name", max_length=100)
    leader = models.UUIDField("Leader's UUID")
    notes = models.CharField("Additional Notes", max_length=255, blank=True)


class Package(models.Model):
    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def __str__(self):
        """
        Returns a string of the package ID.

        :return: package ID of instance as string
        :rtype: str
        """
        return str(self.id)

    # Package properties
    receiving_date = models.DateTimeField('Date Received')
    return_address = models.CharField('Return Address', max_length=200)
    delivery_address = models.CharField('Delivery Address', max_length=200)
    from_nation = models.ForeignKey(Nation, on_delete=models.RESTRICT, related_name="from_nation",
                                    verbose_name="From Nation")
    to_nation = models.ForeignKey(Nation, on_delete=models.RESTRICT, related_name="to_nation", verbose_name="To Nation")
    has_tracking = models.BooleanField("No Tracking", default=False, editable=False)


class Tracking(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "Tracking"

    def __str__(self):
        """
        Returns a string of the tracking code.

        :return: tracking code of instance as string
        :rtype: str
        """
        return str(f"{self.tracking_code} ({self.package.id})")

    readonly_fields = ('package',)

    # Constant Status Codes
    PRE_SHIP = 'XPS'  # Shipping label has been generated
    RECEIVED = 'XRC'  # Package has been received and is being processed
    TRANSIT_FINAL = 'DTD'  # Domestic package is in transit to destination
    TRANSIT_DIST = 'ITD'  # International package is in transit to the distribution centre
    WAITING_DIST = 'IWD'  # International package is awaiting delivery to destination nation
    TRANSIT_INT = 'ITN'  # International package is in transit to destination nation
    DELIVERED = 'XFD'  # Package has been delivered to the destination

    # Choices for statuses
    STATUS_CHOICES = [
        (PRE_SHIP, 'Pre-Shipment'),
        (RECEIVED, 'Received'),
        (TRANSIT_FINAL, 'In Transit (Domestic)'),
        (TRANSIT_DIST, 'In Transit to Distribution Centre'),
        (WAITING_DIST, 'At Distribution Centre'),
        (TRANSIT_INT, 'In Transit to Nation'),
        (DELIVERED, 'Delivered')
    ]

    # Tracking Properties
    tracking_code = models.UUIDField('Tracking Code', primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField('Current Status', max_length=3, choices=STATUS_CHOICES, default=PRE_SHIP)
    package = models.OneToOneField(Package, on_delete=models.CASCADE)

    def status_to_name(self):
        STATUSES = {x[0]: x[1] for x in self.STATUS_CHOICES}
        if self.status in STATUSES:
            return STATUSES[self.status]
        else:
            return False

    # TODO: Maybe add a history feature


class Subscriber(models.Model):
    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.username

    # Subscriber properties
    username = models.CharField("Subscriber's Username", max_length=16)
    uuid = models.CharField("Subscriber's UUID", blank=True, max_length=32)
    email = models.EmailField("Subscriber's Email")
    welcome_email_sent = models.BooleanField("Welcome email sent", default=False, editable=False)
    subscriptions = models.ManyToManyField(Tracking, blank=True)

    def welcome_email(self):
        send_mail(
            subject='Thanks for signing up for WL Post!',
            message=f'Hello {self.username},\n'
                    f'Thank you for signing up to receive tracking notifications from WL Post!\n'
                    f'We will be sending updates regarding your package shortly.\n'
                    f'\n'
                    f'Thanks for shipping with WL Post!',
            from_email='noreply@zandercraft.ca',
            recipient_list=[str(self.email)],
            fail_silently=False
        )
        print(f"Welcome email sent to {self.email} ({self.username})")

    def tracking_update_email(self, tracking_code):
        tracking = Tracking.objects.get(tracking_code=tracking_code)
        send_mail(
            subject=f"WL Post Package Update ({tracking_code})",
            message=f"Hello {self.username},\n"
                    f"The status of the package you subscribed to has been updated!\n"
                    f"\n"
                    f"Status: {tracking.status} ({str(tracking.status_to_name())})\n"
                    f"More Details: http://127.0.0.1:8000/track/{tracking.tracking_code}/\n"
                    f"\n"
                    f"Thanks for shipping with WL Post!",
            from_email='noreply@zandercraft.ca',
            recipient_list=[str(self.email)],
            fail_silently=False
        )
        print(f"Tracking update email sent to {self.email} ({self.username})")
