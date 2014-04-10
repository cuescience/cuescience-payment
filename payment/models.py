from django.db import models
from django.utils.translation import ugettext_lazy as _


class Payment(models.Model):
    approved = models.BooleanField(blank=True, default=False)

    def __unicode__(self):
        return _(u"payed") if self.approved else (u"not payed")

class PayPalPayment(Payment):
    paypal_payment_id = models.CharField(max_length=256, blank=True)
    approval_url = models.CharField(max_length=256, blank=True)

