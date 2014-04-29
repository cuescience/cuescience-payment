from django.contrib import admin
from payment.models import PrePayment, PayPalPayment

admin.site.register(PrePayment)
admin.site.register(PayPalPayment)