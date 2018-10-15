from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    class Meta:
        permissions = (
            ('can_create_view_via_API', 'Create or View via API'),
            ('can_view_via_API', 'Create View only via API'),
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Payment(models.Model):

    msisdn = models.CharField(
        pgettext_lazy('Payment field', 'MSISDN (e.g 254708374149)'),
        blank=True, null=True, max_length=255)
    first_name = models.CharField(
        pgettext_lazy('Payment field', 'FirstName'),
        blank=True, null=True, max_length=255)
    middle_name = models.CharField(
        pgettext_lazy('Payment field', 'MiddleName'),
        blank=True, null=True, max_length=255)
    last_name = models.CharField(
        pgettext_lazy('Payment field', 'LastName'),
        blank=True, null=True, max_length=255)
    trans_time = models.CharField(
        pgettext_lazy('Payment field', 'TransTime (e.g 20181009075311)'),
        blank=True, null=True, max_length=255)
    trans_id = models.CharField(
        pgettext_lazy('Payment field', 'TransID (e.g MJ951H6YF7)'),
        blank=True, null=True, max_length=255, unique=True)
    trans_amount = models.CharField(
        pgettext_lazy('Payment field', 'TransAmount (e.g 100.00)'),
        blank=True, null=True, max_length=255)
    org_account_balance = models.CharField(
        pgettext_lazy('Payment field', 'OrgAccountBalance (e.g 518663.00)'),
        blank=True, null=True, max_length=255)
    invoice_number = models.CharField(
        pgettext_lazy('Payment field', 'InvoiceNumber'),
        blank=True, null=True, max_length=255)
    bill_ref_number = models.CharField(
        pgettext_lazy('Payment field', 'BillRefNumber e.g(account name - testapi)'),
        blank=True, null=True, max_length=255)
    third_party_transid = models.CharField(
        pgettext_lazy('Payment field', 'ThirdPartyTransID'),
        blank=True, null=True, max_length=255)
    business_short_code = models.CharField(
        pgettext_lazy('Payment field', 'BusinessShortCode (e.g 600520)'),
        blank=True, null=True, max_length=255)
    transaction_type = models.CharField(
        pgettext_lazy('Payment field', 'TransactionType (e.g Pay Bill)'),
        blank=True, null=True, max_length=255)
    status = models.IntegerField(
        pgettext_lazy('Payment field', 
            'status( [0 - not picked], [1 - picked], [2 -inserted to db] )'),
        default=0)

    updated_at = models.DateTimeField(
        pgettext_lazy('Payment field', 'date of update'),
        auto_now=True, null=True)

    created_at = models.DateTimeField(pgettext_lazy('Payment field', 'date of create'),
                                   default=now, editable=False)

    class Meta:
        verbose_name = pgettext_lazy('Payment model', 'Mpesa Payment')
        verbose_name_plural = pgettext_lazy('Payment model', 'Mpesa Payment')

    def __str__(self):
        return self.trans_id

